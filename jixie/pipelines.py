# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook
from jixie import settings
import pymongo
#
# class JixiePipeline(object):
#
#     def __init__(self):
#         self.wb = Workbook() # class实例化
#         self.ws = self.wb.active # 激活工作表
#         self.ws.append(['职位','公司','公司类型','地区','经验','学位','薪水','职位描述']) # 添加第一行的数据
#     def process_item(self, item, spider):
#         line = [item['job'],item['company'],item['company_type'],item['area'],item['experience'],item['degree'],item['salary'],item['describe']]
#         self.ws.append(line)
#         self.wb.save('E:\Python_exercise\练习\机械相关数据分析/51.xlsx') # 保存文件
#         return item

class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def process_item(self,item,spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item
    def close_spider(self,spider):
        self.client.close()
