# coding=utf-8

"""
日志处理文件
按天生产文件
"""

import logging
from logging import handlers

# 日志级别关系映射
LEVEL_RELATIONS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR
}

FORMAT_STR = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class SpiderLogger(object):
    """ 按照时间自动分割日志文件 """

    def __init__(self, filename, level='info', when='D', back_count=7):
        self.logger = logging.getLogger(filename)
        # 设置日志级别
        self.logger.setLevel(LEVEL_RELATIONS.get(level))
        # 往文件里写入#指定间隔时间自动生成文件的处理器
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=back_count, encoding='utf-8')
        # 设置日志格式
        th.setFormatter(FORMAT_STR)
        # 把对象加到logger里
        self.logger.addHandler(th)

        # 往屏幕上输出
        sh = logging.StreamHandler()
        # 设置屏幕上显示的格式
        sh.setFormatter(FORMAT_STR)
        self.logger.addHandler(sh)


class DateFileLogger(object):
    """ 这里按照脚本执行程序，所以按日期指定日志文件名 """

    def __init__(self, filename, level='info'):
        self.logger = logging.getLogger(filename)
        # 设置日志级别
        self.logger.setLevel(LEVEL_RELATIONS.get(level))

        # open的打开模式这里可以进行参考，默认追加的方式写入日志
        fh = logging.FileHandler(filename, mode='a')
        # 设置格式
        fh.setFormatter(FORMAT_STR)
        # 把对象加到logger里
        self.logger.addHandler(fh)

        # 往屏幕上输出
        # sh = logging.StreamHandler()
        # 设置屏幕上显示的格式
        # sh.setFormatter(FORMAT_STR)
        # self.logger.addHandler(sh)


if __name__ == '__main__':
    log = DateFileLogger('./log/test.log', level='info')
    log.logger.debug("all debug:", )
    log.logger.info("all info: %s" % 777)
    log.logger.warning("all warn")
    log.logger.error("all error")
    #
    # SpiderLogger('../error.log', level='error').logger.error('error')
