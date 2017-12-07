#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 11:49
# @Author  : Smile
# @Describe:


import hashlib
from time import time
import requests


class Translate:
    @staticmethod
    def md5(str):  # 生成md5
        m = hashlib.md5()
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def translate(text, form="zh", to="jp"):
        appid = '20171207000102908'
        pwd = 'SaoFzsvl_uIEmmSIwgdt'
        salt = str(int(time()))
        all = appid + text + salt + pwd
        sign = Translate.md5(all)
        text = text.replace(' ', '+')

        url = 'http://api.fanyi.baidu.com/api/trans/vip/translate?q=' \
              + text + "&from=" + form + "&to=" + to + "&appid=" + appid + "&salt=" + salt + "&sign=" + sign
        try:
            r = requests.get(url)
            r.encoding = 'utf-8'
            reqjson = r.json()
            result = reqjson['trans_result'][0]['dst']
            return result
        except:
            return "出错了"
