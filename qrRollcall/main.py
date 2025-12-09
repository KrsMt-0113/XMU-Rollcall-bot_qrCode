import json, threading, uuid, time, socket, os
from queue import Queue, Empty
from flask import Flask, request, jsonify, render_template
from pyngrok import ngrok
from parse_code import parse_sign_qr_code
from xmulogin import xmulogin
from urllib.parse import urlparse, parse_qs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = BASE_DIR + "/qrRollcall/config.json"

with open(CONFIG_PATH) as f:
    cfg = json.load(f)

NGROK_TOKEN = cfg.get("ngrok_token")
SESSION_TIMEOUT = int(cfg.get("session_timeout", 180))
USERNAME = cfg.get("username")
PASSWORD = cfg.get("password")
url = "https://lnt.xmu.edu.cn"
base_url = url

if not NGROK_TOKEN:
    raise SystemExit("config.json 中未找到 ngrok_token")

ngrok.set_auth_token(NGROK_TOKEN)

app = Flask(__name__)
sessions = {}
login_session = None  # 存储登录后的 session


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def scan_url_analysis(e: str):
    print(f"scanUrlAnalysis url: {e}")

    if "/j?p=" in e and not e.startswith("http"):
        e = base_url + e

    if not e.startswith("http"):
        return e

    try:
        n = urlparse(e)
    except Exception:
        return e

    if n.path in ["/j", "/scanner-jumper"]:
        o = parse_qs(n.query)
        r = None
        try:
            a = o.get("_p", [None])[0]
            if a:
                r = json.loads(a)
        except Exception:
            pass

        if not r:
            p_value = o.get("p", [""])[0]
            r = parse_sign_qr_code(p_value)

        return json.dumps(r) if r and isinstance(r, dict) and r else e

    return e

@app.route("/scan/<sid>")
def scan_page(sid):
    if sid not in sessions:
        return "会话不存在或过期", 404
    return render_template("scan.html", sid=sid)


@app.route("/submit/<sid>", methods=["POST"])
def submit(sid):
    if sid not in sessions:
        return jsonify({"ok": False, "message": "会话无效或已过期"}), 404
    data = request.get_json(force=True)
    text = data.get("text")
    if not text:
        return jsonify({"ok": False, "message": "没有二维码内容"}), 400
    sessions[sid].put(text)
    return jsonify({"ok": True, "message": "已收到二维码内容"})


@app.route("/_shutdown", methods=["POST"])
def _shutdown():
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        func()
        return "shutting down"
    return "no shutdown func", 500

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def create_session(timeout=SESSION_TIMEOUT):
    sid = uuid.uuid4().hex
    q = Queue()
    sessions[sid] = q
    def expire():
        time.sleep(timeout)
        if sid in sessions:
            print(f"会话 {sid} 已过期，正在删除")
            try:
                sessions[sid].put(None)
            except:
                pass
            del sessions[sid]
    threading.Thread(target=expire, daemon=True).start()
    return sid, q

def run_flask():
    app.run(host="0.0.0.0", port=5001, debug=False, use_reloader=False)

if __name__ == "__main__":
    session = xmulogin(type=3, username=USERNAME, password=PASSWORD)
    if session:
        print("登录成功！")
        login_session = session  # 将登录session保存到全局变量
    else:
        print("登录失败，程序终止。")
        time.sleep(1)
        exit()

    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(1)
    local_ip = get_local_ip()

    tunnel = ngrok.connect("5001")

    tunnels = ngrok.get_tunnels()

    https_url = None
    http_url = None

    for t in tunnels:
        if t.public_url.startswith("https://"):
            https_url = t.public_url
        elif t.public_url.startswith("http://"):
            http_url = t.public_url

    if https_url:
        public_base = https_url.rstrip("/")
        print("ngrok HTTPS 隧道已建立:", public_base)
    elif http_url:
        public_base = http_url.rstrip("/")
        print("ngrok HTTP 隧道已建立:", public_base)
        print("警告：使用 HTTP，浏览器可能无法访问摄像头。请在 localhost 或使用 ngrok 的 HTTPS 端点。")
    else:
        public_base = tunnel.public_url.rstrip("/")
        print("ngrok 隧道已建立:", public_base)

    clear_console()

    try:
        while True:
            sid, q = create_session()
            link = f"{public_base}/scan/{sid}"
            print("一次性扫码链接（有效期 %ds）：" % SESSION_TIMEOUT)
            print(link)
            print("等待扫码并回传数据...")

            try:
                result = q.get(timeout=SESSION_TIMEOUT + 5)
                # print("链接:", result) # 调试用
                # print("解析后链接:", scan_url_analysis(result)) # 调试用
                data = json.loads(scan_url_analysis(result))
            except Empty:
                print("超时，未收到扫码数据。")
                continue

            if result is None:
                print("会话被过期或取消。")
                continue

            if result:
                rollcall_url = f"{url}/api/rollcall/{data['rollcallId']}/answer_qr_rollcall"
                print("签到接口地址:", rollcall_url) # 调试用
                body = {
                    "data": data['data'],
                    "deviceId": str(uuid.uuid4()),
                }
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36 Edg/141.0.0.0",
                    "Content-Type": "application/json"
                }

                res = session.put(rollcall_url, headers=headers, json=body)

                if res.status_code == 200:
                    print("二维码签到成功!")
                    break
                else:
                    print("签到失败，服务器返回状态码:", res.status_code)
                    print(res.json())

    finally:
        try:
            ngrok.kill()
        except:
            pass