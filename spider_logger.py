# coding=utf-8

"""
日志处理文件
按天生产文件
"""

import logging
from logging import handlers


class SpiderLogger(object):
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }

    def __init__(self, filename, level='info', when='D', back_count=7):
        self.logger = logging.getLogger(filename)
        # 设置日志格式
        format_str = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 往文件里写入#指定间隔时间自动生成文件的处理器
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=back_count, encoding='utf-8')
        th.setFormatter(format_str)
        # 把对象加到logger里
        self.logger.addHandler(th)

        # 往屏幕上输出
        sh = logging.StreamHandler()
        # 设置屏幕上显示的格式
        sh.setFormatter(format_str)
        self.logger.addHandler(sh)


if __name__ == '__main__':
    log = SpiderLogger('../test.log', level='info')
    # log.logger.debug("all debug:",)
    log.logger.info("all info:{%s}" % (777))
    # log.logger.warning("all warn")
    # log.logger.error("all error")
    #
    # SpiderLogger('../error.log', level='error').logger.error('error')
