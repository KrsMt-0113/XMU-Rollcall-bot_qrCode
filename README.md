# `Rollcall-bot qrCode version 0.1`

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