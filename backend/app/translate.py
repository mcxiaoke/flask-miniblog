# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
import time
from app.config import TRANSLATE_APP_KEY, TRANSLATE_APP_SECRET

YOUDAO_URL = 'https://openapi.youdao.com/api'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def translate(q, from_lng='en', to_lng='zh-CHS'):

    data = {}
    data['from'] = from_lng
    data['to'] = to_lng
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = TRANSLATE_APP_KEY + \
        truncate(q) + salt + curtime + TRANSLATE_APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = TRANSLATE_APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    response = do_request(data)
    return response.json()['translation'][0]


if __name__ == '__main__':
    print(translate(TEXT))
