# -*- coding: utf-8 -*-
import logging.config
import time

import leancloud

us_stock_list = ['GOOG', 'AMZN', 'FB', 'AAPL', 'BABA', 'TSLA', '00700']
leancloud.init("OiLSQcrjrx0bGhil1d6cxn4c-gzGzoHsz", "qlxrzsclqoUw1Htl5xSXRETI")

StockPrice = leancloud.Object.extend('StockPrice')

logging.config.fileConfig("logger.conf")
logger = logging.getLogger('example')

stock_map = {
    'GOOG': '谷歌',
    'AMZN': '亚马逊',
    'FB': '脸书',
    'AAPL': '苹果',
    'BABA': '阿里巴巴',
    'TSLA': '特斯拉',
    '00700': '腾讯',
}

date = ''



def save(code, price):
    global date
    if not check_stock_price_exist(code, date):
        stock_price = StockPrice()
        stock_price.set('code', code)
        stock_price.set('price', float(price))
        stock_price.set('date', date)
        stock_price.set('name', stock_map[code])
        try:
            stock_price.save()
        except Exception as e:
            logger.error(str(e))
    else:
        logger.info('already exists, date is {}'.format(date))


def check_stock_price_exist(code, date):
    query1 = StockPrice.query
    query2 = StockPrice.query
    query1.equal_to('date', date)
    query2.equal_to('code', code)
    query = leancloud.Query.and_(query1, query2)
    return query.count() > 0


if __name__ == '__main__':
    prices = []
    date = input('please enter date:')
    for code in us_stock_list:
        prices.append((code, float(input('please enter the price for %s: ' % code))))
    for price in prices:
        save(price[0], price[1])