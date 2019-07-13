# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class JixieItem(scrapy.Item):
    # 定义抓取的字段
    job = Field()
    company = Field()
    company_type = Field()
    area = Field()
    experience = Field()
    degree = Field()
    salary = Field()
    describe = Field()





    pass
