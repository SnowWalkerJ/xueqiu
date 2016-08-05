import requests
import re
import sys
import json
import hashlib
import cookielib
from common.db.mongo import *
from startpro.core.utils.loader import get_settings
from startpro.common.utils.log4py import log


class Crawler(object):
    def __init__(self):
        self._session = requests.session()
        self._token = None
        self.headers = {
            'User-Agent': get_settings("browser-agent"),
            'Referer': get_settings("browser-referer"),
            'X-Requested-With': 'XMLHttpRequest',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
            "Connection": "keep-alive",
        }

    @staticmethod
    def get_md5(password):
        md5 = hashlib.md5()
        md5.update(password.encode())
        return md5.hexdigest().upper()

    @property
    def session(self):
        return self._session

    @property
    def cookies(self):
        return self.session.cookies

    @property
    def token(self):
        if not self._token:
            self._token = self.get_token()
        return self._token

    def get_token(self):
        headers = {
            'Host': 'api.xueqiu.com',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Proxy-Connection': 'keep-alive',
            'Cookie': '',
            'User-Agent': 'Xueqiu iPhone 7.6',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Length': '274',
        }
        data = {
            '_': '1460546975217',
            'client_id': 'WiCimxpj5H',
            'client_secret': 'TM69Da3uPkFzIdxpTEm6hp',
            'grant_type': 'password',
            'sid': 'A3BFC63C-B5A3-4FD2-85DA-BA354E28ACDB',
            'sign': '117a9c51f70fa07796b92d16b606176a09926a07',
            'timestamp': '1460546975000',
            'trace_id': '0A3BFC63C-B5A3-4FD2-85DA-BA354E28ACDB',
            'type': '2',
            'version': '0706002',
        }

        url = 'https://api.xueqiu.com/provider/oauth/token'

        resp = self.session.post(url, data=data, headers=headers)
        resp = json.loads(resp.content)
        token = resp.get('access_token')
        return token

    def get_netvalue(self):
        mongo = get_mongo_collection("xueqiu/netvalue")
        for code in self.iter_code():
            try:
                url = get_settings("netvalue_url") % (code, self.token)
                resp = self.session.get(url, headers=self.headers).content
                resp = json.loads(resp)[0]
                if code % 1000 == 0:
                    log.info("netvalue %s:%s" % (resp['symbol'], resp['name']))
                mongo.insert(resp)
            except:
                s = sys.exc_info()
                log.error('get_netvalue %s on line %d' % (s[1], s[2].tb_lineno))

    def get_change_position(self):
        mongo = get_mongo_collection("xueqiu/change_position")
        for code in self.iter_code():
            try:
                data = []
                page = 1
                while page:
                    url = get_settings("change_position_url") % (code, page, self.token)
                    resp = self.session.get(url, headers=self.headers).content
                    resp = json.loads(resp)
                    data += resp['list']
                    if resp['count'] * page <= resp['totalCount']:
                        page += 1
                    else:
                        page = 0
                mongo.insert(dict(symbol="ZH%d" % code, data=data))
                if code % 1000 == 0:
                    log.info("change_position ZH%d" % code)
            except:
                s = sys.exc_info()
                log.error('get_change_position %s on line %d' % (s[1], s[2].tb_lineno))

    @staticmethod
    def iter_code():
        rng = get_settings("code_range")
        start, end = rng.split(":")
        start, end = int(start), int(end)
        return xrange(start, end)


