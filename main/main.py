from common.crawler import Crawler
from startpro.core.utils.loader import safe_init_run


@safe_init_run
def run(**kwargs):
    crawler = Crawler()
    print crawler.token
    # print crawler.get_xsrf(), crawler.is_login()
    # crawler.load_cookies()
    #crawler.get_netvalue()
    crawler.get_change_position()
