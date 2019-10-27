import requests
import re
from common.constants import FAKE_HEADERS

"""解析网页相关方法"""


def get_html(url):
    """
    获取网页
    :param url: 连接地址
    :return: html
    """
    response = requests.get(url, headers=FAKE_HEADERS)
    if response.status_code == 200:
        return response.text
    return None


def analysis_price(price):
    """
    解析具体价格为数字类型
    :param price: 价格描述
    :return: number
    """
    price = re.search(r'\d+(\.\d+)?', price)
    if price:
        return price.group()
    else:
        return 0
