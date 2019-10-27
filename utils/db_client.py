# -*- coding: utf-8 -*-

# 数据库连接类
import pymongo


class MongoDbUtil(object):
    """MongoBD相关操作"""

    def __init__(self, host='localhost', port=27017, db=None, collection=None):
        # ip
        self.host = host
        # 端口
        self.port = port
        # 连接对象
        self.client = None
        # 指定数据库
        self.db = db
        # 指定集合（对应MySql的表）
        self.collection = collection

    def connect_mongo(self):
        """连接MongoDB"""
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        db = self.client[self.db]
        collection = db[self.collection]
        return collection

    def save_to_mongo(self, data_list):
        """
        存入MongoDB
        :param data_list: 数据列表
        """
        self.collection.insert(data_list)

    def close_mongo(self):
        """关闭MongoDB连接"""
        self.client.close()
