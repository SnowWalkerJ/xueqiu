import pymongo.connection
from startpro.core.utils.loader import get_settings
from startpro.common.utils.log4py import log

_mongo = None


def get_mongo():
    global _mongo
    if not _mongo:
        mongo_host = get_settings("mongo_host")
        _mongo = pymongo.connection.MongoClient(mongo_host)
    return _mongo


def get_mongo_db(dbname):
    mongo = get_mongo()
    db = mongo.get_database(dbname)
    mongo_user = get_settings("mongo_user")
    mongo_pass = get_settings("mongo_pass")
    if mongo_user:
        try:
            db.authenticate(mongo_user, mongo_pass)
        except:
            log.error("Login MongoDB server failed")
    return db


def get_mongo_collection(cname):
    dbname, collection_name = cname.split("/")
    return get_mongo_db(dbname)[collection_name]
