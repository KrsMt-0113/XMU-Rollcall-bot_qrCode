# `Rollcall-bot qrCode version 0.1`

### [简体中文](README_CN.md)

### step 1: Install requirements

```bash
  pip install -r requirements.txt
```

### step 2: Fill in the configuration file

Fill your info in `config.json`

```aiignore
{
  "username": "your_username",
  "password": "your_password",
  "ngrok_token": "your_ngrok_token",
  "session_timeout": 180
}
```

### step 3: Run the bot

```bash
  python main.py
```

### step 4: Follow the instructions to complete

- The bot will start a local server and provide you with a **ngrok URL**.

- Send the temporary link to **who is in the classroom** and let them scan the QR code.

- If the terminal shows "签到成功!", it means the roll call was successful, you can **double-check on your phone**.

    - Else, resend the **new generated link** to your classmates.