# https://login.anjuke.com/login/form?history=aHR0cHM6Ly9qeC5hbmp1a2UuY29tLz9waT1QWi1iYWlkdS1wYy1hbGwtYmlhb3Rp

"""
todo 待开发
登录接口：
https://cloud-passport.anjuke.com/ajk/login/pc/dologin

POST

id="sdkSubmitForm"
input  name = token

username:
password:
token:
source:
path:
domain:
finger2:
psdk-d:
psdk-v:
callback:

"""
from pyquery import PyQuery as pyQuery
import requests
import time

LOGIN_URI = "https://login.anjuke.com/login/form?history=aHR0cHM6Ly9qeC5hbmp1a2UuY29tLw=="


def login():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }
    # uri = "https://cloud-passport.anjuke.com/ajk/mobile/init?source=ajk-anjuke-pc&path=https%253A%252F%252Flogin.anjuke.com%252Flogin%252Fiframeform%252F&psdk-d=jsdk&psdk-v=1.0.1&callback=JsonpCallBack" + str(
    #     time.time_ns() // 1000)
    response = requests.get(LOGIN_URI, headers=headers)
    f = open("index.html", mode='w', encoding='utf-8')
    f.write(response.text)
    f.close()


login()
