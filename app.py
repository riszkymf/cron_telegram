#! /usr/bin/env python3

import requests
import os
import json
from datetime import datetime

CHAT_ID = os.environ.get("CHAT_ID", os.getenv('CHAT_ID',''))
BOT_ID = os.environ.get("BOT_ID", os.getenv('BOT_ID',''))
REPORT_TELEGRAM = os.environ.get("TELEGRAM_REPORT")

URL_TARGET = os.environ.get("URL_TARGET", os.getenv('URL_TARGET','http://www.google.com'))
REQ_HEADERS = os.environ.get("REQ_HEADERS", os.getenv('REQ_HEADERS','Access-Token: token'))

def dump_log(data):
    _path = os.path.abspath(os.path.dirname(__file__))
    path = _path + '/log/cron.log'
    data = "\n" + json.dumps(data)
    with open(path,"a+") as f:
        f.write(data)



def sync(url,headers=dict()):
    res = requests.get(url, headers=headers, verify=False)
    print("synchronization result : ")
    print(res)
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
    return msg 

def send_to_telegram(chat_id,bot_id,msg):
    if REPORT_TELEGRAM == '1':
        message = {
            "chat_id": str(chat_id),
            "text" : msg
            
        }
        headers = {"Content-Type":"application/json"}
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(bot_id)
        res = requests.post(url=url,headers=headers,data=json.dumps(message))
        return res
    else:
        return False

def get_headers():
    heads = REQ_HEADERS.split(',')
    header = dict()
    for i in heads:
        _header = i.split(": ")
        key = _header[0]
        val = _header[1]
        header.update({key: val})
    return header

try:
    send_to_telegram(CHAT_ID,BOT_ID,"executing cronjob")
except Exception as e:
    print(str(e))
try:
    sync_data = sync(URL_TARGET,get_headers())
except Exception as ee:
    print(str(e))
res = send_to_telegram(CHAT_ID,BOT_ID,sync_data)
dump_log(sync_data)
print("telegram response : ",res)
# if isinstance(res['result'],str):
#     unsorted = json.loads(res['result'])
# elif isinstance(res['result'],dict):
#     unsorted = res['result']

# try:
#     msg = {
#         "ods": unsorted['data']['ods'],
#         "hostbill": {
#             "status": unsorted['data']['hostbill']['status'],
#             "length": len(unsorted['data']['hostbill']['result']),
#             "fail_count": len(unsorted['data']['hostbill']['fails'])
#         },
#         "count": len(unsorted['data']['result'])
#     }
# except Exception as e:
#     msg = {"error" : str(e)}
# res['result']['data'] = msg
