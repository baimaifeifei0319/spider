#coding=utf-8
__author__ = 'sixkery'

import requests, time
from fake_useragent import UserAgent
from lxml import etree
from pandas import DataFrame


# 定义一个装饰器，查看运行时间
def run_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print('运行时间{}'.format(end - start))

    return wrapper


class LianJia():
    def __init__(self):
        self.headers = {'User-Agent': UserAgent().chrome}
        self.num = 1  # 计数用的
        self.data = list()

    def str_to_dict(self):
        head = '''
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
        Accept-Encoding: gzip, deflate, br
        Accept-Language: zh-CN,zh;q=0.9
        Cache-Control: no-cache
        Connection: keep-alive
        Cookie: TY_SESSION_ID=4bea2cab-85ca-404c-938c-1a3a2e7151f7; lianjia_uuid=bdd2833c-74ff-4d8b-8a60-c5c697d7e1d2; _smt_uid=5bb33924.2c270b81; _ga=GA1.2.299343175.1538472229; UM_distinctid=16634173923519-0e53e8d32db969-5e442e19-100200-16634173926666; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1541470858; _jzqc=1; all-lj=c32edd623b8a5a59c7de54c92107bb6c; _qzjc=1; TY_SESSION_ID=56733985-2bd1-4e0e-9c82-323aed168a92; select_city=310000; _jzqckmp=1; _gid=GA1.2.1508780241.1542417647; lianjia_ssid=c9e37931-3ba0-481f-aa14-1942777d27d4; _jzqa=1.2318817490154803000.1538472229.1542417645.1542446728.10; _jzqx=1.1538472229.1542446728.4.jzqsr=google%2Ecom%2Ehk|jzqct=/.jzqsr=sh%2Elianjia%2Ecom|jzqct=/zufang/pg%7b%7d/; CNZZDATA1253492439=1707637694-1538468289-https%253A%252F%252Fbj.lianjia.com%252F%7C1542446728; CNZZDATA1254525948=685621401-1538471236-https%253A%252F%252Fbj.lianjia.com%252F%7C1542446572; CNZZDATA1255633284=868856814-1538471249-https%253A%252F%252Fbj.lianjia.com%252F%7C1542444014; CNZZDATA1255604082=18076908-1538468889-https%253A%252F%252Fbj.lianjia.com%252F%7C1542444515; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1542448421; _qzja=1.76074912.1538472408515.1542417645255.1542446727824.1542446727824.1542448421448.0.0.0.29.10; _qzjb=1.1542446727824.2.0.0.0; _qzjto=4.2.0; _jzqb=1.2.10.1542446728.1
        Host: sh.lianjia.com
        Pragma: no-cache
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
        '''
        headers = {}
        head = head.split('\n')
        for h in head:
            h = h.strip()
            if h:
                k, v = h.split(':', 1)
                headers[k] = v.strip()
        return headers

    # 获取详情页的 url
    def get_html(self):
        for page in range(10):
            url = 'https://sh.lianjia.com/zufang/page{}/'.format(page)
            print('正在爬取第{}页'.format(page + 1))
            response = requests.get(url, headers=self.str_to_dict())
            if response.status_code == 200:
                html = etree.HTML(response.text)
                urls = html.xpath('//*[@id="house-lst"]/li/div[2]/h2/a/@href')
                for url in urls:
                    # time.sleep(1)
                    print(url)
                    print('爬取第{}条数据'.format(self.num))
                    result = self.parse_page(url)
                    self.num += 1
                    self.data.append(result)


    # 解析详情页并提取具体字段
    def parse_page(self, url):
        result = {}
        response = requests.get(url, headers=self.headers)
        print(response.text)
        html = etree.HTML(response.text)
        result['价格'] = html.xpath('//div[4]/div[2]/div[2]/div[1]/span[1]/text()')[0]
        result['面积'] = html.xpath('//div[4]/div[2]/div[2]/div[2]/p[1]/text()')[0]
        result['楼层'] = html.xpath('//div[4]/div[2]/div[2]/div[2]/p[3]/text()')[0]
        result['房屋户型'] = html.xpath('//div[4]/div[2]/div[2]/div[2]/p[2]/text()')[0]
        result['房屋朝向'] = html.xpath('//div[4]/div[2]/div[2]/div[2]/p[4]/text()')[0]
        result['地铁'] = html.xpath('//div[4]/div[2]/div[2]/div[2]/p[5]/text()')[0]
        result['小区'] = html.xpath('//div[4]/div[2]/div[2]/div[2]/p[6]/a[1]/text()')[0] + ' ' + \
                       html.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[6]/a[2]/text()')[0]
        result['位置'] = html.xpath('//div[4]/div[2]/div[2]/div[2]/p[7]/a[1]/text()')[0] + ' ' + \
                       html.xpath('//div[4]/div[2]/div[2]/div[2]/p[7]/a[2]/text()')[0]

        print(result)
        return result

    @run_time
    def run(self):
        self.get_html()

        # 保存数据到 CSV
        data = DataFrame(self.data)
        data.to_csv('上海租房信息.csv', encoding='utf_8_sig', index=None)


if __name__ == '__main__':
    LianJia().run()


