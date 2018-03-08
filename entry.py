# -*- coding: utf-8 -*-
import logging.config
import time

import leancloud
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

us_stock_list = ['GOOG', 'AMZN', 'FB', 'AAPL', 'BABA', 'TSLA']
us_url = 'http://stock.finance.sina.com.cn/usstock/quotes/{}.html'
hk_stock_list = ['00700']
hk_url = 'http://stock.finance.sina.com.cn/hkstock/quotes/{}.html'
leancloud.init("OiLSQcrjrx0bGhil1d6cxn4c-gzGzoHsz", "qlxrzsclqoUw1Htl5xSXRETI")
dcap = dict(DesiredCapabilities.PHANTOMJS)
PHANTOMJS_PATH = 'D:\\Python\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'
# PHANTOMJS_PATH = "/home/lsm/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"

StockPrice = leancloud.Object.extend('StockPrice')

logging.config.fileConfig("logger.conf")
logger = logging.getLogger('example')


def crawl_us(url, code):
    logger.info('start get {} stock price job'.format(code))
    dcap[
        "phantomjs.page.settings.userAgent"] = \
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
    driver = webdriver.PhantomJS(PHANTOMJS_PATH, desired_capabilities=dcap)
    driver.get(url)
    time.sleep(2)
    try:
        logger.info('get {} stock price'.format(code))
        price = float(driver.title.split(' ')[1].split('(')[0])
        save(code, price)
        driver.quit()
    except Exception as e:
        logger.error(str(e))
        driver.quit()


def crawl_hk(url, code):
    logger.info('start get {} stock price job'.format(code))
    dcap[
        "phantomjs.page.settings.userAgent"] = \
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"
    driver = webdriver.PhantomJS(PHANTOMJS_PATH, desired_capabilities=dcap)
    driver.get(url)
    time.sleep(2)
    try:
        driver.save_screenshot('pic1.png')
        title = driver.title
        logger.info('get {} stock price'.format(code))
        price = float(title.split(' ')[2].split('(')[0])
        save(code, price)
        driver.quit()
    except Exception as e:
        logger.error(str(e))
        driver.quit()


def save(code, price):
    date = time.strftime("%Y%m%d", time.localtime())
    if not check_stock_price_exist(code, date):
        stock_price = StockPrice()
        stock_price.set('code', code)
        stock_price.set('price', float(price))
        stock_price.set('date', date)
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
    logger.info('daily work started')
    for s in us_stock_list:
        crawl_us(us_url.format(s), s)
    for s in hk_stock_list:
        crawl_hk(hk_url.format(s), s)
