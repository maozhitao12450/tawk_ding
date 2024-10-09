from flask import Flask, request
import requests
import json
import os
app = Flask(__name__)

class DingTalk:
    def __init__(self):
        self.__headers = {'Content-Type': 'application/json;charset=utf-8'}
        self.url = os.getenv('TAWK_DINGDING_URL')
 
    def send_msg(self, text):
        json_text = {
                "msgtype": "text",
                "text": {
                "content":  os.getenv('TAWK_DINGDING_SIGN') + ": \n" + text            ## 写入要传送的内容
            },
                "at": {
                "atMobiles": [""],
                "isAtAll": False
            }
        }
        return requests.post(self.url, json.dumps(json_text), headers=self.__headers).content

@app.route('/', methods=['POST'])
def dingding():
    # 读取body中的信息转换为json格式
    data = json.loads(request.get_data())
     # 读取id字段
    property = data.get('property')
    if property:
        if property.get("name") == os.getenv('TAWK_DINGDING_SIGN'):
            # 发送消息
            ding = DingTalk()
            send_message = ""
            message = data.get('message')
            if message:
                send_message = message.get('text')
            response = ding.send_msg('event: ' + data.get('event') +'\n message: ' +send_message)
            return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('TAWK_DINGDING_PORT')))
