#coding=utf-8
__date__ = ' 21:21'
__author__ = 'sixkery'

'''为了简单就获取 APP 端的数据'''

import requests, json
from datetime import datetime
from fake_useragent import UserAgent
from models import ArticleModelUtils


# 今日头条的分类
categories = {
    "news_hot": "热点",
    "news_image": "图片",
    "news_entertainment": "娱乐",
    "news_tech": "科技",
    "news_car": "汽车",
    "news_sports": " 体育",
    "news_finance": "财经",
    "news_military": "军事",
    "news_world": "国际",
    "news_fashion": "时尚",
    "news_travel": "旅游",
    "news_discovery": "探索",
    "news_baby": "育儿",
    "news_regimen": "养生",
    "news_essay": "美文",
    "news_game": "游戏",
    "news_history": "历史",
    "news_food": "美食",
    "news_story": "故事",
    "news_career": "职业",
    "news": "新闻",
    "news_society": "社会",
    "news_culture": "文化",
    "emotion": "情感",
    "news_agriculture": "农村",
    "video_domestic": "视频",
    "news_pet": "宠物",
    "news_house": "房产",
    "news_novel": "小说",
    "news_investment": "环境",
    "news_edu": "教育",
    "funny": "搞笑",
    "news_health": "健康",
    "news_politics": "政治",
    "immigration": "移民",
    "news_photography": "美图",
    "general_positive_video": "视频",
    "science_all": "科学",
    "lottery": "彩票",
}


def crawl_toutiao():
    url = 'https://lf.snssdk.com/api/news/feed/v88/'
    headers = {'User-Agent':UserAgent().chrome}
    r = requests.get(url,headers=headers,verify=False)
    for row in r.json().get('data'):
        content = json.loads(row.get('content'))
        title = content.get('title')
        source = content.get('source')
        item_id = content.get('item_id')
        article_url = 'https://www.toutiao.com/a{}/'.format(item_id)
        summary = content.get('abstract')
        tag = content.get('tag')
        user_id = content.get('user_info').get('user_id')
        source_url = "https://www.toutiao.com/c/user/{}/".format(user_id)
        publish_time = content.get('publish_time')
        publish_time = datetime.fromtimestamp(publish_time).strftime('%Y-%m-%d %H:%M:%S')
        image = content.get('middle_image',{}).get('url')

        item = {
            'title':title,
            'article_url':article_url,
            'source':source,
            'source_url':source_url,
            'summary':summary,
            'tag':categories.get(tag,tag),
            'publish_time':publish_time,
            'image':image
        }

        yield item

def crawl():
    count = 0
    for item in crawl_toutiao():
        ret = ArticleModelUtils.insert(item)
        if ret is True:
            count += 1
    return count


if __name__ == '__main__':
    crawl()