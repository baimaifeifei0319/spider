#coding=utf-8

__author__ = 'sixkery'

''' MongoEngine 是 MongoDB 的 DOM（Document-Object Mapper）框架，一种类似于关系型数据库中的ORM框架 '''
from datetime import datetime

from mongoengine import DateTimeField, Document, IntField, StringField, URLField, connect

# 连接 mongodb
connect('weixin',host='localhost',port=27017)

class Post(Document):
    '''文章的信息'''
    title = StringField() # 标题
    content_url = StringField() # 文章链接
    content = StringField() # 内容
    source_url = StringField() # 原文链接
    digest = StringField() # 文章摘要
    cover = URLField(validation=None) # 封面图
    p_date = DateTimeField() # 发布时间

    read_num = IntField(default=0) # 阅读数
    like_num = IntField(default=0)# 喜欢数
    author = StringField() # 作者

    c_date = DateTimeField(default=datetime.now) # 数据生成时间
    u_date = DateTimeField(default=datetime.now) # 数据更新时间

