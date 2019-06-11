from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent,MessageEvent,TextMessage,TextSendMessage,ImageMessage,ImageSendMessage,TemplateSendMessage,ButtonsTemplate,PostbackTemplateAction,MessageTemplateAction,URITemplateAction
import os

port = os.environ['PORT']

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

pattern_dict = {}

@app.route('/callback',methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    print(body)
    app.logger.info("Request body:"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    if event.message.text in pattern_dict:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=pattern_dict[event.message.text]))
    else:
        pass
def prepare_dict():
    with open("./static/pattern.txt") as file:
        for line in file:
            kv = line.split(None,1)
            pattern_dict[kv[0].strip()] = kv[1].strip()


if __name__ == '__main__':
    prepare_dict()
    app.run(host='0.0.0.0',port=port)
