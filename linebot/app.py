import os
import logging
from dotenv import load_dotenv

from flask import Flask, request, abort, jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# Configure logging
logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

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
        app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    app.logger.info(f"Received message: {event.message.text}")
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))

@app.route("/send_message", methods=['POST'])
def send_message():
    data = request.json
    group_id = data.get('group_id')
    user_id = data.get('user_id')
    message = data.get('message')
    
    if not message:
        app.logger.error("Message is required")
        return jsonify({'error': 'message is required'}), 400
    
    if group_id:
        target_id = group_id
    elif user_id:
        target_id = user_id
    else:
        app.logger.error("Group ID or User ID is required")
        return jsonify({'error': 'group_id or user_id is required'}), 400
    
    try:
        line_bot_api.push_message(target_id, TextSendMessage(text=message))
        app.logger.info(f"Message sent to {'group' if group_id else 'user'}: {target_id}")
        return jsonify({'status': 'message sent'}), 200
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()