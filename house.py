from pyquery import PyQuery as pyQuery
import time
from html_utils import get_html, analysis_price
import pymongo
from spider_logger import SpiderLogger
import traceback
from mail_notice import send_mail

"""
安居客房源信息统计（楼盘+二手房）
"""

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
# 用户验证时需要
AUTH_USER = "admin"
AUTH_PWD = "123456"


class NewHouse(object):
    """
    新楼盘统计
    """

    def __init__(self, report_date):
        self.report_date = report_date
        self.db_name = 'spiders'
        self.collection_name = 'new_house'
        self.collection = None
        self.total = 0
        self.new_log = SpiderLogger('./log/new_house.log', level='info')

    def analyze_info(self, url):
        """
        解析数据
        :param url: 网页地址
        """
        house_list = []
        doc = pyQuery(get_html(url))
        items = doc('.key-list .item-mod').items()
        for item in items:
            address = item.find('.address').text()
            # 去空格
            index = address.find('\xa0', 2)
            address = ' '.join(address.split())
            # 地区
            city = ''
            if index >= 2:
                city = address[2:index]
            # 价格
            price_desc = item.find('.price').text() or item.find('.price-txt').text()
            house_info = {
                # 城市
                'city': city,
                # 名称
                'name': item.find('.lp-name h3').text(),
                # 户型
                'house_type': ' '.join(item.find('.huxing').text().split()),
                # 地址
                'address': address,
                # 地址链接
                'address_link': item.find('.address').attr('href'),
                # 标签
                'tags': item.find('.tag-panel').text(),
                # 价格
                'price': price_desc,
                'price_nu': analysis_price(price_desc),
                # 排名
                'rank': item.find('.group-mark').text(),
                # 图片
                'pic': item.find('.pic img').attr('src'),
                # 图片链接
                'pic_link': item.children('.pic').attr('href'),
                'report_date': self.report_date
            }
            # 加入列表中
            house_list.append(house_info)
        self.total += len(house_list)
        # 本页数据批量存入MongoDB中
        self.collection.insert(house_list)
        # 获取下一页，如果有下一页的，继续爬取下一页的内容
        next_url = doc('.list-page .next-page').attr('href')
        if next_url:
            time.sleep(2)
            self.new_log.logger.info('next => %s' % next_url)
            self.analyze_info(next_url)

    def run_spider(self):
        client = None
        try:
            # 连接mongoDB 默认localhost:27017
            # client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT, username=AUTH_USER, password=AUTH_PWD)
            client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
            db = client[self.db_name]
            self.collection = db[self.collection_name]

            self.new_log.logger.info('new start ... 清空今日楼盘数据 => %s' % self.report_date)
            self.collection.remove({'report_date': self.report_date})

            # 首页地址
            url = 'https://jx.fang.anjuke.com/loupan/all/'
            # 解析网页，并存储数据
            self.analyze_info(url)

            self.new_log.logger.info('end new <= %s，total: %s' % (self.report_date, self.total))
        except BaseException as e:
            self.new_log.logger.error("%s new error %s____%s" % (self.report_date, BaseException, e))
            self.new_log.logger.error(traceback.format_exc())
            send_mail('webCrawler', '执行楼盘任务异常：' + traceback.format_exc())
        finally:
            # 关闭mongodb连接
            client.close()
            self.new_log.logger.info('close mongodb new')


class SaleHouse(object):
    """
    二手房统计
    """

    def __init__(self, report_date):
        self.report_date = report_date
        self.db_name = 'spiders'
        self.collection_name = 'sale_house'
        self.collection = None
        self.total = 0
        self.sale_log = SpiderLogger('./log/sale_house.log', level='info')

    def analyze_info(self, url):
        """
        解析数据
        :param url: 网页源码
        """
        house_list = []
        doc = pyQuery(get_html(url))
        items = doc('#houselist-mod-new .list-item').items()
        for item in items:
            detail = ' '.join(item.find('.details-item').text().split()).split(' ')
            if len(detail) < 3:
                continue
            all_price_desc = item.find('.price-det').text()
            unit_price_desc = item.find('.unit-price').text()
            house_info = {
                # 区域
                'city': detail[2].split('-')[0],
                # 名称
                'name': detail[1],
                # 户型
                'house_type': detail[0][0:detail[0].find('造') + 1],
                # 地址
                'address': detail[2],
                # 标签
                'tags': item.find('.tags-bottom').text(),
                # 总价
                'all_price': all_price_desc,
                'all_price_nu': analysis_price(all_price_desc),
                # 单价
                'unit-price': unit_price_desc,
                'unit-price_nu': analysis_price(unit_price_desc),
                # 图片
                'pic': item.find('.item-img img').attr('src'),
                # 房源真实性
                'authenticity': item.find('.house-title .house-icon').text(),
                'report_date': self.report_date
            }
            # 加入列表中
            house_list.append(house_info)
        self.total += len(house_list)
        # 批量存入MongoDB中
        self.collection.insert(house_list)
        # 获取下一页，如果有下一页的，继续爬取下一页的内容
        next_url = doc('.multi-page .aNxt').attr('href')
        if next_url:
            time.sleep(2)
            self.sale_log.logger.info('next => %s' % next_url)
            self.analyze_info(next_url)

    def run_spider(self):
        client = None
        try:
            # 连接mongoDB 默认localhost:27017
            # client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT, username=AUTH_USER, password=AUTH_PWD)
            client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
            db = client[self.db_name]
            self.collection = db[self.collection_name]

            print('sale start ... 清空今日二手房数据：', self.report_date)
            self.collection.remove({'report_date': self.report_date})

            # 首页地址
            url = 'https://jx.anjuke.com/sale/'
            # 解析源码，并存储数据
            self.analyze_info(url)

            self.sale_log.logger.info('end sale <= %s，total: %s' % (self.report_date, self.total))
        except BaseException as e:
            self.sale_log.logger.error("%s sale error %s____%s" % (self.report_date, BaseException, e))
            self.sale_log.logger.error(traceback.format_exc())
            send_mail('webCrawler', '执行二手房任务异常：' + traceback.format_exc())
        finally:
            # 关闭mongodb连接
            client.close()
            self.sale_log.logger.info('close mongodb sale')
