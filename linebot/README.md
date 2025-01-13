# LINE BOT Setup

## Table of Contents

- [kjnews folder](#kjnews-folder)
- [LINE bot](#line-bot)
- [Setup ngrok (Ubuntu)](#setup-ngrok-ubuntu)
- [Inside the kjnews folder](#inside-the-kjnews-folder)
  - [.env](#env)
  - [app.py](#apppy)
  - [ngrok_startup.sh](#ngrok_startupsh)
- [Using Systemd To Run Scripts When Startup](#using-systemd-to-run-scripts-when-startup)
- [References](#references)
  - [LINE](#line)

## *kjnews* folder
```
kjnews
│   .env
│   requirements.txt
│   ngrok_startup.sh
│   app.py
│   log.log
└───venv
```

## LINE bot
Create a LINE bot from [LINE Official Account Manager](https://manager.line.biz/). Then enable `Allow bot to join group chats`, disable `Auto-reply messages` and `Greeting messages` in the console. 

## Setup ngrok (Ubuntu)
Ref: [ngrok webiste](https://ngrok.com/), [ngrok docs](https://ngrok.com/docs/guides/device-gateway/linux/)

Install the ngrok Agent
```shell=
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
sudo tar xvzf ./ngrok-v3-stable-linux-amd64.tgz -C /usr/local/bin
ngrok authtoken NGROK_AUTHTOKEN
```

## Inside the *kjnews* folder

### .env
Issue `CHANNEL_ACCESS_TOKEN` and get `CHANNEL_SECRET` from [Messaging API](https://developers.line.biz/console/). 

### app.py
Use venv by `python -m venv venv`, and install requirements inside `requirements.txt`. 

### ngrok_startup.sh
Replace `<ngrok-url>` from *[Static Domain](https://dashboard.ngrok.com/get-started/setup/linux)*. 

## Using Systemd To Run Scripts When Startup
1. Create a Systemd Service file:
`sudo nano /etc/systemd/system/kjnews.service`
2. Add the following content to the file: 
    ```=
    [Unit]
    Description=Startup script for KJNews and Ngrok
    After=network.target

    [Service]
    Type=simple
    ExecStart=/bin/bash -c '/home/<username>/kjnews/venv/bin/python /home/<username>/kjnews/app.py & /bin/bash /home/<username>/kjnews/ngrok_startup.sh'
    Restart=always
    RestartSec=5
    User=<username>
    WorkingDirectory=/home/<username>/kjnews

    [Install]
    WantedBy=multi-user.target
    ```
3. Reload Systemd configuration
`sudo systemctl daemon-reload`
4. Start the service
`sudo systemctl start kjnews.service`
`sudo systemctl status kjnews.service`
5. Set the auto-start function
`sudo systemctl enable kjnews.service`
6. Log View (Optional)
`journalctl -u kjnews.service -f`

## References
- [建立並串接 Webhook](https://steam.oxxostudio.tw/category/python/example/line-webhook.html)
- [使用 Requests 傳送訊息](https://steam.oxxostudio.tw/category/python/example/line-requests.html)
- [( Day 39.1 ) Python LINE BOT 建立並串接 Webhook](https://ithelp.ithome.com.tw/articles/10336795)
- [( Day 39.2 ) Python LINE BOT 解析 LINE 的訊息](https://ithelp.ithome.com.tw/articles/10336837)
- [( Day 40.2 ) Python LINE BOT 主動推播訊息](https://ithelp.ithome.com.tw/articles/10337875)
- [LINE 聊天機器人 - 手把手教學，輕鬆學會模仿與互動的功能 on GCP Cloud Functions](https://medium.com/@chiehwen0926/line-%E8%81%8A%E5%A4%A9%E6%A9%9F%E5%99%A8%E4%BA%BA-%E8%BC%95%E9%AC%86%E6%A8%A1%E4%BB%BF%E8%88%87%E4%BA%92%E5%8B%95%E7%9A%84%E7%B5%82%E6%A5%B5%E6%8C%87%E5%8D%97-gcp-cloud-functions-%E6%87%89%E7%94%A8%E5%AF%A6%E4%BE%8B-d4f43db3ca67)
- [Create a Line Chatbot (01)](https://medium.com/%E5%B7%A5%E7%A8%8B%E9%9A%A8%E5%AF%AB%E7%AD%86%E8%A8%98/create-a-line-chatbot-on-gcp-ecc3c9d2674d)
- [DAY 7 回話機器人(鸚鵡LINE Bot)與ngrok](https://ithelp.ithome.com.tw/articles/10295654)

### LINE
- [LINE Official Account Manager](https://manager.line.biz/)
- [LINE Developer Console](https://developers.line.biz/console/)