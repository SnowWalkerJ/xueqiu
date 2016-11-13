import tushare as ts
from common.crawler import Crawler
from startpro.core.utils.loader import safe_init_run
import sys


def get_all_stocks():
    data = ts.get_stock_basics()        # get the stock list from tushare
    for stock in data.index:
        if stock[0] == '6':
            stock_id = 'SH%s' % stock   # add prefix
        else:
            stock_id = "SZ%s" % stock
        yield stock_id


def worker(stock_id):
    try:
        crawler = Crawler()
        crawler.get_stock_comment(stock_id)
        print stock_id
    except:
        s = sys.exc_info()
        print ('worker %s on line %d.' % (s[1], s[2].tb_lineno))

@safe_init_run
def run(**kwargs):
    try:
        for stock_id in get_all_stocks():
            worker(stock_id)
    except:
        s = sys.exc_info()
        print ('run %s on line %d.' % (s[1], s[2].tb_lineno))

