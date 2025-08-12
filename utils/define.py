from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 功能1：回原文
def echo_message(msg):
    return TextSendMessage(text=msg)
