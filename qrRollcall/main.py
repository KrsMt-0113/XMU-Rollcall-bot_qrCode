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
session_cookies = {}

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
const cookies = {{ cookies|safe }};
const url = "https://lnt.xmu.edu.cn";

// 解析二维码数据的函数
function parseSignQrCode(t) {
  const ta = String.fromCharCode(30);
  const ea = String.fromCharCode(31);
  const na = String.fromCharCode(26);
  const ra = String.fromCharCode(16);
  const ia = na + "1";
  const oa = na + "0";
  
  const aa = {};
  ["courseId", "activityId", "activityType", "data", "rollcallId",
   "groupSetId", "accessCode", "action", "enableGroupRollcall", "createUser",
   "joinCourse"].forEach((key, i) => {
    aa[key] = i.toString(36);
  });
  
  const ua = {};
  ["classroom-exam", "feedback", "vote"].forEach((key, i) => {
    ua[key] = na + (i + 2).toString(36);
  });
  
  const ca = {};
  for (let k in aa) ca[aa[k]] = k;
  const sa = {};
  for (let k in ua) sa[ua[k]] = k;
  
  const result = {};
  if (t && typeof t === "string") {
    const parts = t.split("!").filter(p => p);
    for (let part of parts) {
      const idx = part.indexOf("~");
      if (idx > 0) {
        const r = part.substring(0, idx);
        const i = part.substring(idx + 1);
        const key = ca[r] || r;
        let value;
        if (i.startsWith(na)) {
          if (i === ia) {
            value = true;
          } else if (i !== oa) {
            value = sa[i] || i;
          } else {
            value = false;
          }
        } else if (i.startsWith(ra)) {
          const parts_ = i.substring(1).split(".");
          try {
            const nums = parts_.map(p => parseInt(p, 36));
            if (nums.length > 1) {
              value = parseFloat(nums[0] + "." + nums[1]);
            } else if (nums.length === 1) {
              value = nums[0];
            } else {
              value = i;
            }
          } catch (e) {
            value = i;
          }
        } else {
          value = i.replace(new RegExp(ea, 'g'), "~").replace(new RegExp(ta, 'g'), "!");
        }
        result[key] = value;
      }
    }
  }
  return result;
}

// 生成UUID
function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

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

async function signIn(qrData) {
  try {
    const parsedData = parseSignQrCode(qrData);
    console.log("解析的数据:", parsedData);
    
    if (!parsedData.rollcallId || !parsedData.data) {
      return { status_code: 400, message: "二维码数据不完整" };
    }
    
    const signUrl = `${url}/api/rollcall/${parsedData.rollcallId}/answer_qr_rollcall`;
    const body = {
      data: parsedData.data,
      deviceId: generateUUID()
    };
    
    // 将cookies转换为字符串格式
    let cookieStr = "";
    for (let key in cookies) {
      if (cookieStr) cookieStr += "; ";
      cookieStr += key + "=" + cookies[key];
    }
    
    const response = await fetch(signUrl, {
      method: "PUT",
      headers: {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36 Edg/141.0.0.0",
        "Content-Type": "application/json",
        "Cookie": cookieStr
      },
      body: JSON.stringify(body),
      credentials: "include"
    });
    
    const status = response.status;
    let message = "";
    
    if (status === 200) {
      message = "签到成功!";
    } else {
      message = `签到失败，状态码: ${status}`;
    }
    
    return { status_code: status, message: message };
  } catch (e) {
    console.error("签到错误:", e);
    return { status_code: 500, message: "签到请求失败: " + e.message };
  }
}

function tick() {
  if (video.readyState === video.HAVE_ENOUGH_DATA) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(data.data, data.width, data.height);
    if (code) {
      msg.textContent = "已识别，正在签到…";
      stopCamera();
      
      signIn(code.data).then(result => {
        msg.textContent = result.message;
        
        // 将状态码发送回服务器
        fetch(submitUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(result)
        }).then(r => r.json()).then(j => {
          console.log("服务器响应:", j);
        }).catch(e => {
          console.error("发送状态失败:", e);
        });
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

@app.route("/scan/<sid>")
def scan_page(sid):
    if sid not in sessions:
        return "会话不存在或过期", 404
    cookies_json = json.dumps(session_cookies.get(sid, {}))
    return render_template_string(HTML_TEMPLATE, sid=sid, cookies=cookies_json)

@app.route("/submit/<sid>", methods=["POST"])
def submit(sid):
    if sid not in sessions:
        return jsonify({"ok": False, "message": "会话无效或已过期"}), 404
    data = request.get_json(force=True)
    status_code = data.get("status_code")
    message = data.get("message", "")
    if status_code is None:
        return jsonify({"ok": False, "message": "缺少状态码"}), 400
    # 将状态码和消息放入队列
    sessions[sid].put({"status_code": status_code, "message": message})
    return jsonify({"ok": True, "message": "状态已接收"})

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

def create_session(cookies, timeout=SESSION_TIMEOUT):
    sid = uuid.uuid4().hex
    q = Queue()
    sessions[sid] = q
    session_cookies[sid] = cookies
    def expire():
        time.sleep(timeout)
        if sid in sessions:
            print(f"会话 {sid} 已过期，正在删除")
            try:
                sessions[sid].put(None)
            except:
                pass
            del sessions[sid]
            if sid in session_cookies:
                del session_cookies[sid]
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
            sid, q = create_session(verified_cookies)
            link = f"{public_base}/scan/{sid}"
            print("一次性扫码链接（有效期 %ds）：" % SESSION_TIMEOUT)
            print(link)
            print("等待扫码和签到...")

            try:
                result = q.get(timeout=SESSION_TIMEOUT + 5)
            except Empty:
                print("超时，未收到签到结果。")
                continue

            if result is None:
                print("会话被过期或取消。")
                continue

            if result and isinstance(result, dict):
                status_code = result.get("status_code")
                message = result.get("message", "")
                print(f"收到签到结果: 状态码 {status_code} - {message}")
                
                if status_code == 200:
                    print("二维码签到成功!")
                    break
                else:
                    print(f"签到失败，状态码: {status_code}, 消息: {message}")
            else:
                print("收到无效的响应格式")

    finally:
        try:
            ngrok.kill()
        except:
            pass