# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from lxml import etree
import re
from jixie.items import JixieItem

class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']
    keyword = quote('机械')
    headers = {
        'Host': 'search.51job.com',
        'Referer': 'https://www.51job.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
       }

    def start_requests(self):
        '''获取开始抓取的页面'''
        for i in range(1,5):
            url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,'+ self.keyword + ',2,{}.html'.format(str(i))
            yield scrapy.Request(url=url,headers=self.headers,callback=self.parse_detial_url)

    def parse_detial_url(self,response):
        '''获取详情页的url'''
        s = etree.HTML(response.text)
        detail_urls = s.xpath('//*[@id="resultList"]/div/p/span/a/@href')
        for detial_url in detail_urls:
            url = detial_url
            yield scrapy.Request(url=url,headers=self.headers,callback=self.parse)

    def parse(self, response):
        '''解析详情页具体字段'''
        item = JixieItem() # 实例化类
        s = etree.HTML(response.text)
        jobs = s.xpath('//div[@class="tHeader tHjob"]/div/div[1]/h1/text()')
        if jobs:
            item['job'] = jobs[0].strip()
        else:
            item['job'] = ''
        companys = s.xpath('//div[@class="tHeader tHjob"]/div/div[1]/p[1]/a[1]/text()')
        if companys:
            item['company'] = companys[0].strip()
        else:
            item['company'] = ''
        company_types = s.xpath('//div[@class="com_tag"]/p/text()')
        if company_types:
            item['company_type'] = company_types[0]
        else:
            item['company_type'] = ''
        data = s.xpath('//div[@class="tHeader tHjob"]/div/div[1]/p[2]/text()')
        if data:
            item['area'] = data[0].strip()
            item['experience'] = data[1].strip()
            item['degree'] = data[2].strip()

        salarys = s.xpath('//div[@class="tHeader tHjob"]/div/div[1]/strong/text()')
        if salarys:
            item['salary'] = salarys[0].strip()
        else:
            item['salary'] = ''
        describes = re.findall(re.compile('<div class="bmsg job_msg inbox">(.*?)div class="mt10"', re.S), response.text)
        if describes:
            item['describe'] = describes[0].strip().replace('<p>', '').replace('</p>','').replace('<p>','').replace('<span>','').replace('</span>','').replace('\t','')
        yield item


