# -*- coding: utf-8 -*-
from flask import Flask, request, abort
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
from linebot.v3.messaging.models import TextMessage, ReplyMessageRequest
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import json
from google.cloud import secretmanager

from utils.deifne import *

# 建立 Flask app
app = Flask(__name__)

def access_secret_version(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    secret_string = response.payload.data.decode("UTF-8")
    return secret_string
    
# 你 GCP 專案 ID
PROJECT_ID = "gen-lang-client-0700041250"

# 從 Secret Manager 取得密鑰
access_token = access_secret_version(PROJECT_ID, "LINE_CHANNEL_ACCESS_TOKEN")
secret = access_secret_version(PROJECT_ID, "LINE_CHANNEL_SECRET")

# 初始化 LineBotApi 與 WebhookHandler
line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)

# 主 Webhook 路由
@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    signature = request.headers.get('X-Line-Signature', '')
    try:
        handler.handle(body, signature)
        json_data = json.loads(body)
        msg = json_data['events'][0]['message']['text']
        tk = json_data['events'][0]['replyToken']
        reply = echo_message(msg)
        line_bot_api.reply_message(tk, reply)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print("Error:", e)
        print("Request body:", body)
    return 'OK'

# 你可以用下面方式直接啟動 flask server (開發測試用)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
