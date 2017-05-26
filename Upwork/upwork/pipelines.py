# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from .items import UpworkItem

class UpworkPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("localhost", port=27017)
        db = client["Upwork"]
        self.UpworkDoc = db["UpworkDoc"]

    def process_item(self, item, spider):
        if isinstance(item, UpworkItem):
            print('UpworkItem True')
            try:
                self.UpworkDoc.insert(dict(item))
            except Exception:
                pass
        return item