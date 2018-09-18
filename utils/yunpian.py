# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/8/8 11:58'

import json
import requests
import random

from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
# 初始化client,apikey作为所有请求的默认值

class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def send_sms(self,code,hour,mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            # "text": "【梅渚个人信息网】亲爱的{name}，您的验证码是{code}。有效期为{hour}，请尽快验证".format(name=name, code=code, hour=hour)
            "text": "【梅渚个人信息网】您的验证码是{code}。有效期为{hour}，请尽快验证，如非本人操作，请忽略本短信。".format(code=code, hour=hour)

        }
        clnt = YunpianClient(parmas["apikey"])
        param = {YC.MOBILE:parmas["mobile"], YC.TEXT:parmas["text"]}
        r = clnt.sms().single_send(param)
        pass
        return r

# 获取返回结果, 返回码:r.code(),返回码描述:r.msg(),API结果:r.data(),其他说明:r.detail(),调用异常:r.exception()
# 短信:clnt.sms() 账户:clnt.user() 签名:clnt.sign() 模版:clnt.tpl() 语音:clnt.voice() 流量:clnt.flow()



def generate_code():

    code = ""
    for i in range(0, 6):
        num=random.randint(0, 9)
        code = code + str(num)

    return code

if __name__ == "__main__":
    yun_pian = YunPian("")
    code = yun_pian.send_sms("201808", "20分钟", "18768114732")
    msg = code._msg
    msg_code = code._code
    # code = generate_code()
    pass
