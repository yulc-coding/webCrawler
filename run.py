from spider.house import NewHouse, SaleHouse
import time


def new_house_spider():
    new_house = NewHouse(int(time.strftime("%Y%m%d", time.localtime())))
    new_house.run_spider()


def sale_house_spider():
    sale_house = SaleHouse(int(time.strftime("%Y%m%d", time.localtime())))
    sale_house.run_spider()


new_house_spider()
sale_house_spider()
