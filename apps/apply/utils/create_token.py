import datetime

import jwt

from pandaHired import settings


def create_token(payload):
    salt=settings.SECRET_KEY
    headers={
        "type":"jwt",
        "alg":"HS256"
    }
    payload["exp"]=datetime.datetime.now()+datetime.timedelta(minutes=1)
    token=jwt.encode(payload=payload,key=salt,algorithm="HS256",headers=headers).decode("utf-8")
    return token