from __future__ import unicode_literals

import os
import sys
import redis
import json
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, PostbackEvent,TextMessage, TextSendMessage, FlexSendMessage,ImageMessage, VideoMessage, FileMessage, FlexSendMessage,
    StickerMessage, StickerSendMessage, TemplateSendMessage, ButtonsTemplate,PostbackAction,MessageAction,BubbleContainer
)
from linebot.utils import PY3

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            if(isinstance(event,PostbackEvent) and event.postback.data=='funcid1'):
                handler_function1((event))
            if(isinstance(event,PostbackEvent) and event.postback.data=='funcid2'):
                handler_function2((event))
            if(isinstance(event,PostbackEvent) and event.postback.data=='funcid3'):
                handler_function3((event))
            if(isinstance(event,PostbackEvent) and event.postback.data[0:5]=='prov_'):
                handler_CityList(event)
            if not isinstance(event,PostbackEvent):
                continue
        else:
            send_InitButton(event)

    return 'OK'
#data/variable initiated by GAO Han
#province list
init_data=[
    "Anhui","Beijing","Chongqing","Fujian","Gansu","Guangdong","Guangxi","Guizhou","Hainan","Hebei","Henan","Heilongjiang",
    "Hubei","Hunan","Nei Mongolia","Jilin","Jiangsu","Jiangxi","Ningxia","Qinghai","Shandong","Shanxi","Shaanxi",
    "Shanghai","Sichuan","Tianjin","Tibet","Xinjiang","Yunnan","Zhejiang"
]
#province content array
prov_cont_array=[]
#data init end

#Generate province content array
#by GAO Han
def prov_ListArray(arr):
    default_action={'type':'postback','label':"default_label",'data':"default_data"}
    default_content={'type':'button',"style":"secondary","height":"sm","margin":"xs"}
    for item in arr:
        prov_item='prov_'+item
        default_action['label']=item
        default_action['data']=prov_item
        default_content['action']=default_action
        content_str=str(default_content)
        dict_temp=eval(content_str)
        prov_cont_array.append(dict_temp)
    return prov_cont_array

#Send initial button message
def send_InitButton(event):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='Home',
                text='Please select a function you need',
                actions=[
                    PostbackAction(
                        label='function1',
                        display_text='function1',
                        data='funcid1'
                    ),
                    PostbackAction(
                        label='function2',
                        display_text='function2',
                        data='funcid2'
                    ),
                    PostbackAction(
                        label='function3',
                        display_text='function3',
                        data='funcid3'
                    )
                ]
            )
        )
    )


#display city list
#by GAO Han
def handler_CityList(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("Please choose cities in "+event.postback.data[5:])
    )

#Handle function1
def handler_function1(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="this is function1!")
    )
#Handle function2
def handler_function2(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="this is a function2!")
    )

#Handle function3--display info about designated hospitals
#step1--display all the provinces/municipality
#by GAO Han
def handler_function3(event):
    con=prov_ListArray(init_data)
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text="list",
            contents={
                "type": "bubble",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents":con
                }
            }
        )
    )
if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)
