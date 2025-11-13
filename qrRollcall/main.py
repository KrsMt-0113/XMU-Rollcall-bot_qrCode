import json, threading, uuid, time, socket, requests, os
from queue import Queue, Empty
from flask import Flask, request, render_template_string, jsonify
from pyngrok import ngrok
from parse_code import parse_sign_qr_code
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from login import login
from get_config import get_config_path

with open(get_config_path()) as f:
    cfg = json.load(f)

NGROK_TOKEN = cfg.get("ngrok_token")
SESSION_TIMEOUT = int(cfg.get("session_timeout", 180))
USERNAME = cfg.get("username")
PASSWORD = cfg.get("password")
url = "https://lnt.xmu.edu.cn"

if not NGROK_TOKEN:
    raise SystemExit("config.json 中未找到 ngrok_token")

ngrok.set_auth_token(NGROK_TOKEN)

app = Flask(__name__)
sessions = {}

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>XMU Rollcall bot - QRcode Scanner</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: #000;
      color: #fff;
      overflow: hidden;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }
    h3 {
      text-align: center;
      padding: 15px;
      background: rgba(0, 0, 0, 0.8);
      font-size: 16px;
      font-weight: normal;
    }
    #video-container {
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: hidden;
    }
    #video {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    #canvas {
      display: none;
    }
    #msg {
      text-align: center;
      padding: 15px;
      background: rgba(0, 0, 0, 0.8);
      font-size: 14px;
      min-height: 50px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  </style>
</head>
<body>
  <h3>对准二维码，识别后自动上传</h3>
  <div id="video-container">
    <video id="video" autoplay playsinline></video>
  </div>
  <canvas id="canvas"></canvas>
  <p id="msg">正在启动相机...</p>
<script src="https://unpkg.com/jsqr/dist/jsQR.js"></script>
<script>
const sid = "{{ sid }}";
const submitUrl = "/submit/" + sid;
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const msg = document.getElementById("msg");

async function start() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: { 
        facingMode: "environment",
        width: { ideal: 1920 },
        height: { ideal: 1080 }
      }
    });
    video.srcObject = stream;
    video.setAttribute("playsinline", true);
    msg.textContent = "请对准二维码扫描";
    requestAnimationFrame(tick);
  } catch (e) {
    msg.textContent = "无法访问相机: " + e.message;
  }
}

function stopCamera() {
  const s = video.srcObject;
  if (s) s.getTracks().forEach(t => t.stop());
}

function tick() {
  if (video.readyState === video.HAVE_ENOUGH_DATA) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(data.data, data.width, data.height);
    if (code) {
      msg.textContent = "已识别，正在上传…";
      stopCamera();
      fetch(submitUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: code.data })
      }).then(r=>r.json()).then(j=>{
        msg.textContent = j.message || "上传完成";
      }).catch(e=>{
        msg.textContent = "上传失败: "+e;
      });
      return;
    }
  }
  requestAnimationFrame(tick);
}

start();
</script>
</body>
</html>
"""

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def parse_url(url: str):
    base_url = "https://c-mobile.xmu.edu.cn/j?p="
    if url.startswith(base_url):
        return url[len(base_url):].replace("%", "\\u00").encode('utf-8').decode('unicode_escape')
    return url

@app.route("/scan/<sid>")
def scan_page(sid):
    if sid not in sessions:
        return "会话不存在或过期", 404
    return render_template_string(HTML_TEMPLATE, sid=sid)

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
    clear_console()

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    print("正在初始化Selenium...")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://lnt.xmu.edu.cn")

    ts = int(time.time() * 1000)
    temp_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
    captcha_url = f"https://ids.xmu.edu.cn/authserver/checkNeedCaptcha.htl?username={USERNAME}&_={ts}"
    res_data = requests.get(captcha_url, headers=temp_header).json()

    login_status, verified_cookies = login(url, driver, res_data['isNeed'], USERNAME, PASSWORD)
    if login_status:
        print("登录成功！")
    else:
        print("登录失败，程序终止。")
        driver.quit()
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
                data = parse_sign_qr_code(parse_url(result))
                print("收到扫码内容 ->", data)
            except Empty:
                print("超时，未收到扫码数据。")
                continue

            if result is None:
                print("会话被过期或取消。")
                continue

            if result:
                f"{url}/api/rollcall/{data['rollcallId']}/answer_qr_rollcall"
                body = {
                    "data": data['data'],
                    "deviceId": str(uuid.uuid4()),
                }
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36 Edg/141.0.0.0",
                    "Content-Type": "application/json"
                }
                res = requests.put(url, headers=headers, data=json.dumps(body), cookies= verified_cookies)
                # 直接put签不上说是，单put签不上说是
                if res.status_code == 200:
                    print("二维码签到成功!")
                    break
                else:
                    print("签到失败，服务器返回状态码:", res.status_code)

    finally:
        try:
            ngrok.kill()
        except:
            pass