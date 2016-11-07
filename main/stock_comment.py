import tushare as ts
from common.crawler import Crawler
from common.db.mysql import get_alchemy_session, create
from common.process import Process
from startpro.core.utils.loader import safe_init_run
from threadpool import ThreadPool as Pool, makeRequests
import sys


def get_all_stocks():
    data = ts.get_stock_basics()
    for stock in data.index:
        if stock[0] == '6':
            stock_id = 'SH%s' % stock
        else:
            stock_id = "SZ%s" % stock
        yield stock_id


def worker(stock_id):
    try:
        crawler = Crawler()
        comments = crawler.get_stock_comment(stock_id)
        session = get_alchemy_session()
        session.add_all(comments)
        session.commit()
        session.flush()
        print stock_id, len(comments)
    except:
        s = sys.exc_info()
        print ('run %s on line %d.' % (s[1], s[2].tb_lineno))

@safe_init_run
def run(**kwargs):
    try:
        create()

        pool = Pool(2)
        reqs = makeRequests(worker, get_all_stocks())
        for req in reqs:
            pool.putRequest(req)
        pool.wait()
        """
        for stock_id in get_all_stocks():
            worker(stock_id)
        """
    except:
        s = sys.exc_info()
        print ('run %s on line %d.' % (s[1], s[2].tb_lineno))

