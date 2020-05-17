from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('1bw/3nO5f4lJ++o8xvu15WmJgqsPgqN0NaUewlGDPS9wMuSAYAYnbEddxjyBBrhPy/KYu0Kg1lNNOYuGuxRWsObmcDz5yPFD/vwKHbgStqehRxfB4iGDglVwhoCm3IYiP7/t20928CvbwHyFoqXOoAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3c5589e9cae642fbda11e02e91b86e2c')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = StickerSendMessage(package_id='1',sticker_id='1')

    if '感情' or '男朋友' or '女朋友' or '愛情' in msg:
        r = '有關感情的事我一律建議分手'
    elif '事業' or '工作' or '上班' in msg:
        r = '有關工作的事我一律建議辭職'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()