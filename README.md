# security-line-chatbot

### Inroduction

A LINE chatbot build-up for RSA encryption & decryption services (database is built upon 1. dataframe, and 2. Spark database).

### Functions

- Encryption: type "$$message$$", then the encrypted message will be sent back, and be stored into dataframe / database
- Decryption: type "@@message@@", then the decrypted message will be sent back, and be stored into dataframe / database
- Log file
  - View: view the last 5 historical encryption or decryption records (personal info only)
  - Clean: clean all individual historical records in the dataframe / database (other users are remained)

### Security chatbot QR code & Demo



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
- Now the project is built. 
  
- Copy the deplyment url with /callback: https://<Heroku_app_name>.herokuapp.com/callback 

- Paste onto LINE Webhook URL (LINE >> Messaging API settings >> Webhook settings) 
  
- Verified as success. (To ensure no runtime error)
  
- Scan the chatbot QR code (LINE >> Messaging API settings >> QR code)

- Can start interacting with the chatbot in the LINE chat room

  
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

- Copy the forwarding url with /callback: https://xxxxxxxx.ngrok.io/callback

- LINE webhook url use & verify

- Paste onto LINE Webhook URL (LINE >> Messaging API settings >> Webhook settings)

- Verified as success. (To ensure no runtime error)

- Scan the chatbot QR code (LINE >> Messaging API settings >> QR code)

- Can start interacting with the chatbot in the LINE chat room


### Issue
  
It seems Heroku does not support Spark. The project chatbot-spark/ can be built on Heroku, but the Heroku app webhook url cannot be verified by LINE.

  
### Reference

- [1] LINE official: https://github.com/line/line-bot-sdk-python

- [2] GitHub tutorial: https://github.com/yaoandy107/line-bot-tutorial?fbclid=IwAR0mGh2jSmQgSUGj9YG1JmvxnkhbtyzguP1IQCgJtxYA9VzDy_e2zmwhTxA

- [3] Blog: ngrok-webhook https://learn.markteaching.com/ngrok-webhook/?fbclid=IwAR1wSIvOFePpGXo7ZghRNiCgujMVAlZ1CnQNrSEe1g4ue3SGv_8cT8wGC1o
