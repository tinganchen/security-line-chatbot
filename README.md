# security-line-chatbot

### Inroduction

A LINE chatbot build-up for RSA encryption & decryption services (database is built upon 1. dataframe, and 2. Spark database).

### QR code & Demo

### Settings

- [LINE developer account](https://developers.line.biz/console/) [1, 2]

- [Heroku account](https://dashboard.heroku.com/apps) [1, 2]

- [ngrok download](https://ngrok.com/) [3]

### Implementation

```shell
git clone https://github.com/tinganchen/security-line-chatbot.git
```

##### 1. Security Chatbot on dataframe + Heroku

- Move to directory <chatbot-df/>

```shell
cd chatbot-df/
```

- Fill in your LINE $channel access token$ & $channel secret$ in L18 & L20 in <app.py>

- Run app.py

```shell
python3 app.py
```
- Create a new app on Heroku & name your <Heroku app name> (see [2])

- Log in Heroku & upload and build the project through git commands
  
```shell
heroku login
git init
heroku git:remote -a <Heroku_app_name>
git add .
git commit -am 'upload'
git push -f heroku master
```
- Now the project is built. Copy the deplyment url with /callback: https://<Heroku_app_name>.herokuapp.com/callback as the LINE Webhook URL (LINE >> Messaging API settings >> Webhook settings) & verify as success.
  
- Scan the chatbot QR code (LINE >> Messaging API settings >> QR code)

- Start interacting with the chatbot in the LINE chat room

  
##### 2. Security Chatbot on Spark database + ngrok

- Move to directory <chatbot-df/>

```shell
cd chatbot-spark/
```
- Fill in your LINE $channel access token$ & $channel secret$ in L18 & L20 in <app.py>

- Run app.py

```shell
python3 app.py
```
- Run ngrok

```shell
cd <directory where ngrok downloaded>
./ngrok http 5000
```

Copy the forwarding url: https://xxxxxxxx.ngrok.io

- LINE webhook url use & verify

- Paste the ngrok forwarding url with /callback: https://xxxxxxxx.ngrok.io/callback as the LINE Webhook URL (LINE >> Messaging API settings >> Webhook settings) & verify as success.

- Scan the chatbot QR code (LINE >> Messaging API settings >> QR code)

- Start interacting with the chatbot in the LINE chat room




### Issues

### Reference

- [1] LINE official: https://github.com/line/line-bot-sdk-python

- [2] GitHub tutorial: https://github.com/yaoandy107/line-bot-tutorial?fbclid=IwAR0mGh2jSmQgSUGj9YG1JmvxnkhbtyzguP1IQCgJtxYA9VzDy_e2zmwhTxA

- [3] Blog: ngrok-webhook https://learn.markteaching.com/ngrok-webhook/?fbclid=IwAR1wSIvOFePpGXo7ZghRNiCgujMVAlZ1CnQNrSEe1g4ue3SGv_8cT8wGC1o
