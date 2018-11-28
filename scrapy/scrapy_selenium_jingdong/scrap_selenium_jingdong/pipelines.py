# -*- coding: utf-8 -*-
import pymongo
from scrap_selenium_jingdong.settings import MONGO_PORT, MONGO_HOST, DB_NAME, SHEET_NAME

class MongoDBPipeline(object):

    def __init__(self):
        mongocli = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        self.db_name = mongocli[DB_NAME]

    def process_item(self, item, spider):
        self.db_name[SHEET_NAME].insert(dict(item))
        return item
