import requests

import datetime
import time
import math

class OpenidUtils(object):

    def __init__(self, jscode):
        self.url = "https://api.weixin.qq.com/sns/jscode2session"
        self.appid = "wxed8c5f3179155a3d"
        self.secret = "765e6e6010a5c8c8ce0330094d1fdcfa"
        self.jscode = jscode

    def get_openid(self):

        url = self.url + "?appid=" + self.appid + "&secret=" + self.secret + "&js_code=" + self.jscode + "&grant_type=authorization_code"
        r = requests.get(url)
        print(url)
        openid = r.json()['openid']

        return openid


from rest_framework.response import Response


def verify(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response({
            "code": 0,
            "data": serializer.data
        })
    return Response({
        "code": 1,
        "data": serializer.errors
    })






def work_time(ftime):
    date1 = datetime.datetime.strptime(ftime, "%Y-%m-%d")
    a = date1.timestamp()
    b = time.time()
    c = (b - a) / 60 / 60 / 24

    if c < 365:

        c = str(math.ceil(c / 30)) + "月"
        return c
    else:
        c = str(math.ceil(c / 365)) + "年"
        return c


