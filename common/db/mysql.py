import MySQLdb
from startpro.core.utils.loader import get_settings
from startpro.common.utils.log4py import log
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_mysql():
    mysql_host = get_settings("mysql_host")
    mysql_user = get_settings("mysql_user")
    mysql_pass = get_settings("mysql_pass")
    try:
        conn = MySQLdb.connect(host=mysql_host, user=mysql_user, passwd=mysql_pass)
        return conn
    except Exception, e:
        log.error("Connection to MySQL server failed: [%s]" % str(e))


def get_alchemy_session():
    sql_conn_string = get_settings("sql_conn_string")
    engine = create_engine(sql_conn_string)

    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    return session


def create():
    from models.stock_comment import BaseModel
    sql_conn_string = get_settings("sql_conn_string")
    engine = create_engine(sql_conn_string, encoding="utf8",  convert_unicode=True)
    try:
        BaseModel.metadata.drop_all(engine)
    except:
        pass
    BaseModel.metadata.create_all(engine)