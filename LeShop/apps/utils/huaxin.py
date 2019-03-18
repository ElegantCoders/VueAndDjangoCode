import requests
import json

class HuaXin(object):
    def __init__(self, account, password):
        # 账号
        self.account = account
        # 密码
        self.password = password
        # 要请求的url
        self.sms_url = "https://sh2.ipyy.com/smsJson.aspx"

    def send_sms(self, code, mobile):
        # 发送短信验证码要传的参数
        params = {
            "account": self.account,
            "password": self.password,
            "mobile": mobile,
            "content": "【秘密】您的验证码是{}。如非本人操作，请忽略本短信！".format(code),
            "sendTime":'',
            "action":'send',
            "extno":'',
        }
        # 发起一个网络请求
        response = requests.post(self.sms_url, data=params)

        ret = json.loads(response.text)
        return ret


if __name__ == '__main__':
    # 测试
    huaxin = HuaXin('kl55','kl558586')
    r = huaxin.send_sms('6789','18230017065')
    print(r)