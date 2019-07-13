import requests,random
from lxml import etree
from bs4 import BeautifulSoup

class Spider():
    '''随机获取一个IP地址'''

    def __get_page(self):
        '''获取数据，添加请求头'''
        url = 'http://www.xicidaili.com/nn/'
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                                     ' (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }
        r = requests.get(url,headers=headers)
        if r.status_code == 200:
            print('爬取成功')
        return r.text

    def __parse_page(self,html):
        '''这里用了两种方式获取解析IP，返回一个ip列表'''
        '''soup = BeautifulSoup(html,'lxml')
        ips = soup.find_all('tr')#先找到节点tr
        ip_list = []
        for i in range(1,len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' +tds[2].text)
        return ip_list'''

        data = etree.HTML(html)
        items = data.xpath('//tr[@class="odd"]')
        ip_list = []
        for item in items:
            ips = item.xpath('./td[2]/text()')[0]
            tds = item.xpath('./td[3]/text()')[0]
            ip_list.append(ips + ':' + tds)
        return ip_list

    def __get_random_ip(self,ip_list):
        proxy_list = []
        for ip in ip_list:
            #遍历ip列表，添加http://
            proxy_list.append('http://' + ip)
        proxy_ip = random.choice(proxy_list) # 随机返回一个ip
        proxies = {'http':proxy_ip} # 构造成字典。
        return proxies

    def run(self):
        html = self.__get_page()
        ip_list = self.__parse_page(html)
        proxy = self.__get_random_ip(ip_list)
        print(proxy)

if __name__ == '__main__':
    spider = Spider()
    spider.run()