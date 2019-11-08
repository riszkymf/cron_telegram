#! /usr/bin/env python3

import requests
import os
import json
from datetime import datetime

CHAT_ID = os.environ.get("CHAT_ID", os.getenv('CHAT_ID',''))
BOT_ID = os.environ.get("BOT_ID", os.getenv('BOT_ID',''))

URL_TARGET = os.environ.get("URL_TARGET", os.getenv('URL_TARGET','http://www.google.com'))
REQ_HEADERS = os.environ.get("REQ_HEADERS", os.getenv('REQ_HEADERS','Access-Token: token'))

def sync(url,headers=dict()):
    res = requests.get(url,headers=headers)
    now = datetime.now()
    str_date = now.strftime("%d/%m/%Y %H:%M:%S")
    msg = {
        "code": str(res.status_code),
        "result": "",
        "datetime": str_date
    }
    try:
        data = res.json()
        msg['result'] = data
    except Exception as e:
        msg['error'] = str(e)
    res = send_to_telegram(CHAT_ID,BOT_ID,msg)
    return res 

def send_to_telegram(chat_id,bot_id,msg):
    message = {
        "chat_id": str(chat_id),
        "text" : msg
        
    }
    headers = {"Content-Type":"application/json"}
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(bot_id)
    res = requests.post(url=url,headers=headers,data=json.dumps(message))
    return res

def get_headers():
    heads = REQ_HEADERS.split(',')
    header = dict()
    for i in heads:
        _header = i.split(": ")
        key = _header[0]
        val = _header[1]
        header.update({key: val})
    return header
    
sync(URL_TARGET,get_headers())