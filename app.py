# Ver1.1.0
# Develop Edition.
# Feature Plan
#   * Deliver a word list
#   * Add a word from Web application

from flask import Flask,request,abort,jsonify
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent,MessageEvent,TextMessage,TextSendMessage,ImageMessage,ImageSendMessage,TemplateSendMessage,ButtonsTemplate,PostbackTemplateAction,MessageTemplateAction,URITemplateAction
import os


port = os.environ['PORT']


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False;

LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# pattern_list = []
pattern_dict = {}

@app.route('/',methods=['GET'])
def index():
    return 'UedaBot'

@app.route('/word/list', methods=['GET'])
def get_list():
    return jsonify(pattern_dict);

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
    res = ''
    for k,v in pattern_dict.items():
        if k in event.message.text:
            res = v
            break
    # res = [x for x in pattern_list if x.input in event.message.text]
    if res:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=res[0]))

def prepare_dict():
    with open("./static/pattern.txt") as file:
        for line in file:
            kv = line.split(None,1)
            # pattern_list.append({'input':kv[0].strip(), 'output':kv[1].strip()})
            pattern_dict[kv[0].strip()] = kv[1].strip()


prepare_dict()
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port)
