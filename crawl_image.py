#coding=utf-8

__author__ = 'sixkery'

import requests, asyncio, aiohttp
import os, time


def run_time(fn):
    '''装饰器，用于查看图片下载运行时间'''
    def wrapper(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        print('运行时间{}'.format(time.time() - start))

    return wrapper


class Crawl_Image:
    def __init__(self):
        self.num = 1
        if '图片' not in os.listdir('.'):
            os.mkdir('图片')
        self.path = os.path.join(os.path.abspath('.'),'图片')
        os.chdir(self.path)

    def str_dict(self):
        '''把字符串转化成字典，通常的请求头一个一个写成字典麻烦'''
        headers = {}
        heads = '''
        authority: unsplash.com
        method: GET
        path: /napi/photos?page=13&per_page=12&order_by=latest
        scheme: https
        accept: */*
        accept-encoding: gzip, deflate, br
        accept-language: zh-CN,zh;q=0.9
        cache-control: no-cache
        cookie: _ga=GA1.2.1867787748.1541257560; uuid=fbe18d60-df79-11e8-af00-9f82294d3e27; xpos=%7B%7D; lsnp=Wn1U1YnKyn4; ugid=45e258e4a27fdb75969611bfa7b6227a5146352; _gid=GA1.2.104984706.1543905667; lux_uid=154390566744470013; _sp_ses.0295=*; _gat=1; _sp_id.0295=4996ac29-9203-4213-a46d-24cf83d147ce.1541257566.9.1543907256.1541399729.fcdb26b7-0b36-4bab-8056-898cc972167e
        dpr: 1
        pragma: no-cache
        referer: https://unsplash.com/
        user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
        viewport-width: 1350
        '''
        heads = heads.split('\n')
        for head in heads:
            head = head.strip()
            if head:
                head_key,head_value = head.split(':',1)
                headers[head_key] = head_value.strip()
        return headers

    def request_url(self,url):
        '''请求网页，获取图片的 url 。因为图片的请求不多，所以用同步就好'''
        r = requests.get(url,headers=self.str_dict())
        if r.status_code == 200:
            return r.json()

    async def get_image(self, url):
        '''异步请求库aiohttp 加快图片 url 的网页请求'''
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            content = await response.read()
            return content

    async def download_image(self,image):
            html = await self.get_image(image[0])
            with open(image[1] + '.jpg','wb') as f:
                f.write(html)
            print('下载第{}张图片成功'.format(self.num))
            self.num += 1

    @run_time
    def run(self):
        for page in range(10):
            url = 'https://unsplash.com/napi/photos?page={}&per_page=12&order_by=latest'.format(page)
            links = self.request_url(url)
            task = [asyncio.ensure_future(self.download_image((link['links']['download'],link['id']))) for link in links]
            # 获取事件循环 Eventloop
            loop = asyncio.get_event_loop()
            # 执行协程
            loop.run_until_complete(asyncio.wait(task))

if __name__ == '__main__':
    crawl_image = Crawl_Image()
    crawl_image.run()
