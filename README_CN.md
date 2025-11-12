# `Rollcall-bot qrCode version 0.1`

### [English](README.md)

### 第一步: 安装依赖

```bash
  pip install -r requirements.txt
```

### 第二步: 填写配置文件

在 `config.json` 中填写配置文件，包括用户名、密码以及 `ngrok token`。

> 关于 `ngrok token` 的获取，请前往 [ngrok官网](https://ngrok.com/) 注册并登录后，在 "Your Authtoken" 选项卡复制即可。

```aiignore
{
  "username": "your_username",
  "password": "your_password",
  "ngrok_token": "your_ngrok_token",
  "session_timeout": 180
}
```

### 第三步 运行主程序

```bash
  python main.py
```

### 第四步 按指示完成操作

- 程序会启动一个本地服务器，以及一个 **ngrok URL**，别人可以通过该 URL 与你的本地服务器交互。

- 程序会生成一个 180 秒有效的临时链接，发送给 **在教室里的同学**，链接打开会请求使用摄像头，让他们扫描二维码即可。

- 如果终端显示 "签到成功!"，表示签到成功，如果不放心，你可以 **在平台上的签到列表进行二次确认**。

    - 如果没成功，也许是因为运气不好扫到了恰好刷新前的二维码，那么这时程序会生成新的临时链接，重新发送给你的同学即可。