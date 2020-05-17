from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
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
    r = '請不要跟我543'
    for d in str(msg) :
        if msg == '感情':
            r = '有關感情的事我一律建議分手'
            break
        elif msg == ['事業', '工作', '打工', '薪水']:
            r = '有關工作的事我一律建議辭職'
            break
        elif msg == ['寵物', '貓', '狗', '鼠']:
            r = '有關寵物的事我一律建議安樂死'
            break
        else:
            sticker_message = StickerSendMessage(
                package_id='1',
                sticker_id='1'
            )
            line_bot_api.reply_message(
                event.reply_token,
                sticker_message)

            break

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()