import MySQLdb
from startpro.core.utils.loader import get_settings
from startpro.common.utils.log4py import log


def get_mysql():
    mysql_host = get_settings("mysql_host")
    mysql_user = get_settings("mysql_user")
    mysql_pass = get_settings("mysql_pass")
    try:
        conn = MySQLdb.connect(host=mysql_host, user=mysql_user, passwd=mysql_pass)
        return conn
    except Exception, e:
        log.error("Connection to MySQL server failed: [%s]" % str(e))