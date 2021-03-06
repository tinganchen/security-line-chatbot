from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from rsa import *
# from spark_db import * 
from pandas_df import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Your LINE Channel Access Token')
# Channel Secret
handler = WebhookHandler('Your LINE Channel Secret')

## DB build up
log_db = log()
log_db.create_table()

## RSA key generation
RSA_Create_Key()

## Emoji use list
emoji_key = ['laugh1', 'laugh2', 'smile', 'congrats', 'clap', 'love', 'point_out', 'cry', 'encrypt', 'decrypt', 'log', 'help']
emoji_info = ['π', 'π', 'π€', 'π', 'π', 'π', 'π', 'π’', 'π', 'π', 'π£', 'β']
emoji_dict = dict(zip(emoji_key, emoji_info))

# η£θ½ζζδΎθͺ /callback η Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# θηθ¨ζ―
@handler.add(PostbackEvent)
def handle_post_message(event):
    postback_message = event.postback.data
    
    reply_messages = []
    
    if 'help' not in postback_message.lower():
        if postback_message in ['encryption', 'decryption']:
            reply_message = TemplateSendMessage(
                alt_text = 'confirm',
                template = ConfirmTemplate(
                    title = f'Confirm {postback_message}',
                    text = f'Confirm {postback_message}',
                    actions = [                              
                        PostbackTemplateAction(
                            label = 'Y',
                            text = 'Y',
                            data = f'{postback_message[:7]}'
                        ),
                        MessageTemplateAction(
                            label = 'N',
                            text = 'N'
                        )
                    ]
                )
            )
            reply_messages.append(reply_message)
        
        elif postback_message == 'log file':
            reply_message = TemplateSendMessage(
                alt_text = 'view log',
                template = ConfirmTemplate(
                    title = 'Log file',
                    text = 'Log file',
                    actions = [                              
                        PostbackTemplateAction(
                            label='View',
                            text='View',
                            data='view_log'
                        ),
                        PostbackTemplateAction(
                            label='Clean',
                            text='Clean',
                            data='clean_log'
                        )
                    ]
                )
            )
            reply_messages.append(reply_message)
            
        elif postback_message in ['view_log', 'clean_log']:
            if postback_message == 'view_log':
                reply_message = TextSendMessage(text = log_db.view(5, event.source.user_id))
                reply_messages.append(reply_message)
                
                reply_message = TextSendMessage(text = f'Enjoy our services!{emoji_dict["smile"]}')
                reply_messages.append(reply_message)
            
            else:
                log_db.clean(event.source.user_id)
                reply_message = TextSendMessage(text = f'Log is cleaned. View log again{emoji_dict["clap"]}.')
                reply_messages.append(reply_message)

                
        elif postback_message in ['encrypt', 'decrypt']:
            reply_message = TextSendMessage(text = f'Please paste your message for {postback_message}ion.')
            reply_messages.append(reply_message)
            
            if postback_message == 'encrypt':
                reply_message = TextSendMessage(text = f'Must be formatted as: \n$$message$$.')
                reply_messages.append(reply_message)
            else:
                reply_message = TextSendMessage(text = f'Must be formatted as: \n@@message@@.')
                reply_messages.append(reply_message)
            
    else:
        reply_message = TextSendMessage(text = 
                                        'Services desciption:\n--------------------\n'
                                        '1. Encryption/Decryption: type the message to be encrypted/decrypted.\n\n'
                                        '2. Log file: you can "view" or "clean" your personal historical records in database.')
        reply_messages.append(reply_message)
        reply_message = TextSendMessage(text = f'{emoji_dict["congrats"]}Enjoy services!\nStart on {emoji_dict["point_out"]}"Menu".')
        reply_messages.append(reply_message)
        
    line_bot_api.reply_message(event.reply_token, reply_messages)
    
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    received_text = event.message.text
    reply_messages = []
    
    if 'menu' in received_text.lower():
        reply_message = TemplateSendMessage(
                alt_text='menu',
                template=ButtonsTemplate(
                    title='Welcome to Security Chatbot!',
                    text=f'Choose one security service {emoji_dict["smile"]}',
                    thumbnail_image_url='https://blogvaronis2.wpengine.com/wp-content/uploads/2019/12/pgp-encryption-hero.png',
                    actions=[
                        PostbackTemplateAction(
                            label=f'{emoji_dict["encrypt"]}  Encryption',
                            text='Encryption',
                            data='encryption'
                        ),
                        PostbackTemplateAction(
                            label=f'{emoji_dict["decrypt"]}  Decryption',
                            text='Decryption',
                            data='decryption'
                        ),
                        PostbackTemplateAction(
                            label=f'{emoji_dict["log"]}  Log file',
                            text='Log file',
                            data='log file'
                        ),
                        PostbackTemplateAction(
                            label=f'{emoji_dict["help"]}  Help',
                            text='Help',
                            data='help'
                        )
                    ]
                )
                )
        reply_messages.append(reply_message)
    

    
    else:
        if '$$' in [received_text[:2], received_text[-2:]]:
            ##print(received_text)
            # RSA
            message = ''.join([i for i in received_text.split('$$') if len(i) > 0])
            cipher_text = RSA_gKey_Encrypt(message)
            
            # store into DB
            row = [event.source.user_id, 'encrypt', message]
            log_db.insert_row(row)
            
            # reply
            reply_message = TextSendMessage(text = f'Message encrypted{emoji_dict["encrypt"]}:')
            reply_messages.append(reply_message)
            reply_message = TextSendMessage(text = f'{cipher_text.decode("utf-8")}')
            reply_messages.append(reply_message)
            reply_message = TextSendMessage(text = f'Enjoy services!{emoji_dict["encrypt"]}\nGo back to {emoji_dict["point_out"]}"Menu" for more services.')
            reply_messages.append(reply_message)
            
       
        elif '@@' in [received_text[:2], received_text[-2:]]:
    
            # RSA
            cipher_text = ''.join([i for i in received_text.split('@@') if len(i) > 0])
            
            try:
                text = RSA_gKey_Decrypt(cipher_text)
                
                # store into DB
                row = [event.source.user_id, 'decrypt', text]
                log_db.insert_row(row)
                
                # reply
                reply_message = TextSendMessage(text = f'Message decrypted{emoji_dict["decrypt"]}:')
                reply_messages.append(reply_message)
                reply_message = TextSendMessage(text = f'{text}')
                reply_messages.append(reply_message)
                reply_message = TextSendMessage(text = f'Enjoy services!{emoji_dict["decrypt"]}\nGo back to {emoji_dict["point_out"]}"Menu" for more services.')
                reply_messages.append(reply_message)
            except:
                reply_message = TextSendMessage(text = f'Invalid. This is not a cipher{emoji_dict["cry"]}.\nPlease resend an already encrypted message, or back to {emoji_dict["point_out"]}"Menu".')
                reply_messages.append(reply_message)
        
            
    
        elif received_text not in ['Y', 'Help', 'View', 'Clean', 'Log file', 'Encryption', 'Decryption']:
            reply_message = TextSendMessage(text = f'Type {emoji_dict["point_out"]} "Menu" and start the services.')
            reply_messages.append(reply_message)
        
        
    line_bot_api.reply_message(event.reply_token, reply_messages)

        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
    