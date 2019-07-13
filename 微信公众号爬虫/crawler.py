#coding=utf-8
__date__ = ' 21:26'
__author__ = 'sixkery'

import requests, json, re, html, time, logging
from datetime import datetime
from models import Post
import utils
from urllib.parse import urlsplit

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Winxin_Crawler:
    def str_to_dict(self):
        '''字符串转换成字典'''
        # 从抓包软件获取的请求头信息
        head = '''
        Host: mp.weixin.qq.com
        Connection: keep-alive
        User-Agent: Mozilla/5.0 (Linux; Android 8.0.0; FRD-AL00 Build/HUAWEIFRD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044428 Mobile Safari/537.36 MMWEBID/3629 MicroMessenger/6.7.3.1360(0x2607033C) NetType/WIFI Language/zh_CN Process/toolsmp
        X-Requested-With: XMLHttpRequest
        Accept: */*
        Referer: https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA3NDk1NjI0OQ==&scene=126&bizpsid=0&devicetype=android-26&version=2607033c&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=1ToLMmDl3QRdeSTProQYkp04M8Dp4lzLXOI79zL%2B4A0VNtsPvxdWZQj7I70Ooxs8&wx_header=1
        Accept-Encoding: gzip, deflate, br
        Accept-Language: zh-CN,en-US;q=0.9,ar-XB;q=0.8
        Cookie: rewardsn=; wxtokenkey=777; wxuin=1022938422; devicetype=android-26; version=2607033c; lang=zh_CN; pgv_pvid=1291433995; tvfe_boss_uuid=08c841fcf5c60786; pass_ticket=1ToLMmDl3QRdeSTProQYkp04M8Dp4lzLXOI79zL+4A0VNtsPvxdWZQj7I70Ooxs8; wap_sid2=CLaa4+cDElxlVGlRS09ia1lOMlN4Y19qQmZMcUlWWmlHZ1NnQUVNRXZCVU1wM3d1MWJZYXo0eU5DYmFjeHc4WmV1MXRkTi0yVkVwQVdFMDhDMzZGTXk2bEc0T2FTdHdEQUFBfjC71ffgBTgNQJVO
        Q-UA2: QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.7.3&TBSVC=43620&CO=BK&COVC=044428&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= FRD-AL00 &RL=1080*1792&OS=8.0.0&API=26
        Q-GUID: 25e18d89c9b867c493ae78eb122188cb
        Q-Auth: 31045b957cf33acf31e40be2f3e71c5217597676a9729f1b

'''
        heads = head.split('\n')
        headers = {}
        for head in heads:
            head = head.strip()
            if head:
                k,v = head.split(':',1)
                headers[k] = v.strip()
        return headers

    def crawl(self, page=0):
        '''爬取公众号文章'''
        # url 中的参数 appmsg_token 是临时的，需要及时更新
        url = 'https://mp.weixin.qq.com/mp/profile_ext?' \
              'action=getmsg&' \
              '__biz=MzA3NDk1NjI0OQ==&' \
              'f=json&' \
              'offset={}&' \
              'count=10&' \
              'is_ok=1&' \
              'scene=126&' \
              'uin=777&' \
              'key=777&' \
              'pass_ticket=1ToLMmDl3QRdeSTProQYkp04M8Dp4lzLXOI79zL%2B4A0VNtsPvxdWZQj7I70Ooxs8&wxtoken=&' \
              'appmsg_token=988_HRK6oWLgVpB%252FsHthnQ2WvaEC_rD9wXeg_zFp1w~~&' \
              'x5=1&' \
              'f=json'.format(str(page))

        headers = self.str_to_dict()
        r = requests.get(url,headers=headers,verify=False)
        result = r.json()
        # 参数 ret 用来判断是否获取到数据
        if result.get('ret') == 0:
            msg_list = result.get('general_msg_list')
            logger.info('抓取数据:offset=%s,data=%s' % (page,msg_list))
            self.save(msg_list)

            has_next = result.get('can_msg_continue')
            # has_next 判断是否有下一页文章
            if has_next == 1:
                next_offset = result.get('next_offset')
                time.sleep(3)
                # 递归调用爬取微信公众号所有信息
                self.crawl(next_offset)
        else:
            print('参数出错，重新获取')
            # 错误消息
            # {"ret":-3,"errmsg":"no session","cookie_count":1}
            logger.error("无法正确获取内容，请重新从Fiddler获取请求参数和请求头")
            exit()

    @staticmethod
    def save(msg_list):
        msg_list = msg_list.replace('\/','/')
        data = json.loads(msg_list)
        msg_list = data.get('list')
        for msg in msg_list:
            p_date = msg.get('comm_msg_info').get('datetime')
            msg_info = msg.get('app_msg_ext_info') # 非图文消息没有这个字段
            if msg_info:
                Winxin_Crawler._insert(msg_info,p_date)
                multi_msg_info = msg_info.get('multi_app_msg_item_list')
                for msg_item in multi_msg_info:
                    Winxin_Crawler._insert(msg_item,p_date)
            else:
                logger.warning(u"此消息不是图文推送，data=%s" % json.dumps(msg.get("comm_msg_info")))

    @staticmethod
    def _insert(item,p_date):
        keys = ('title','author','content_url','digest','cover','source_url')
        sub_data = utils.sub_dict(item,keys)
        post = Post(**sub_data)
        p_date = datetime.fromtimestamp(p_date)
        post['p_date'] = p_date
        logger.info('save data %s' % post.title)
        try:
            post.save()
        except Exception as e:
            logger.error('保存失败 data=%s' % post.to_json(),exc_info=True)

    @staticmethod
    def update_post(post):
        '''post 是从 mongodb 中提取一条数据进行更新'''
        data_url_params = {'__biz': 'MjM5MzgyODQxMQ==', 'appmsg_type': '9', 'mid': '2650367540',
                           'sn': 'ef9c6353a9255dbc00e2beac7f449dad', 'idx': '1', 'scene': '27',
                           'title': 'Python%E5%A5%87%E6%8A%80%E6%B7%AB%E5%B7%A7%EF%BC%8C%E7%9C%8B%E7%9C%8B%E4%BD%A0%E7%9F%A5%E9%81%93%E5%87%A0%E4%B8%AA',
                           'ct': '1511410410',
                           'abtest_cookie': 'AwABAAoADAANAAcAJIgeAGSIHgD8iB4A7IkeAAaKHgAPih4AU4oeAAAA',
                           'devicetype': 'android-24',
                           'version': '/mmbizwap/zh_CN/htmledition/js/appmsg/index3a9713.js', 'f': 'json',
                           'r': '0.04959653583814139', 'is_need_ad': '0', 'comment_id': '1411699821',
                           'is_need_reward': '1', 'both_ad': '0', 'reward_uin_count': '24', 'msg_daily_idx': '1',
                           'is_original': '0', 'uin': '777', 'key': '777',
                           'pass_ticket': 'zpU4AwNXTGS5LfBXFx4NCyMo5YTpSQo9RarrPG3tjhmMaGfORzykNNviX7IlM4i0',
                           'wxtoken': '1922467438', 'clientversion': '26051732',
                           'appmsg_token': '938_0n0in1TAhMHhtZ7zXIOyxTxYXZEFW7ez7tXTmochNzKXa19P3wxK6-C-yM1omM_h7gSMZJmyv7glw98g',
                           'x5': '1'}  # appmsg_token 记得用最新的

        # url转义处理
        content_url = html.unescape(post.content_url)
        # 截取content_url的查询参数部分
        content_url_params = urlsplit(content_url).query
        # 将参数转化为字典类型
        content_url_params = utils.str_to_dict(content_url_params, "&", "=")
        # 更新到data_url
        data_url_params.update(content_url_params)
        body = "is_only_read=1&req_id=0414NBNjylwrVHDydtl3ufse&pass_ticket=zpU4AwNXTGS5LfBXFx4NCyMo5YTpSQo9RarrPG3tjhmMaGfORzykNNviX7IlM4i0&is_temp_url=0"
        data = utils.str_to_dict(body, "&", "=")

        # 通过Fiddler 获取 最新的值
        headers = """
        Host: mp.weixin.qq.com
        Connection: keep-alive
        Content-Length: 137
        Origin: https://mp.weixin.qq.com
        X-Requested-With: XMLHttpRequest
        User-Agent: Mozilla/5.0 (Linux; Android 7.0; MI 5 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043804 Mobile Safari/537.36 MicroMessenger/6.5.23.1180 NetType/WIFI Language/zh_CN
        Content-Type: application/x-www-form-urlencoded; charset=UTF-8
        Accept: */*
        Referer: https://mp.weixin.qq.com/s?__biz=MjM5MzgyODQxMQ==&mid=2650367558&idx=1&sn=b8be74571b14f78d80c062ded89b2d4a&chksm=be9cdd1289eb5404f1b423a135ce5adf5d2cf802a09014b6f407c96b40fdc88ce6e4e0ed8665&scene=27&ascene=0&devicetype=android-24&version=26051732&nettype=WIFI&abtest_cookie=AwABAAoADAANAAcAJIgeAGSIHgD8iB4A7IkeAAaKHgAPih4AU4oeAAAA&lang=zh_CN&pass_ticket=zpU4AwNXTGS5LfBXFx4NCyMo5YTpSQo9RarrPG3tjhmMaGfORzykNNviX7IlM4i0&wx_header=1
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,en-US;q=0.8
        Cookie: pgv_pvi=1680185344; pgv_si=s6583349248; rewardsn=9a0c2a83b30e5994c162; wxtokenkey=71bdfbb7fad39d08d2eb2dece479971297781391293c3c913e74f0f1c4c16971; wxuin=528927841; devicetype=android-24; version=26051732; lang=zh_CN; pass_ticket=zpU4AwNXTGS5LfBXFx4NCyMo5YTpSQo9RarrPG3tjhmMaGfORzykNNviX7IlM4i0; wap_sid2=COGYm/wBElxvYUdHZDdpUlExT2h3MnVTMS1nendPdUlZZ1BsU2h3ZUhibGNNQTRMS0t1dXhPQS1YUHNZNGdhQXk2Z0F0WkF0U3dGVUlYNnBHdlVTVEk0aHBOMktXS29EQUFBfjCyjLfSBTgNQAE=
        Q-UA2: QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.5.23&TBSVC=43602&CO=BK&COVC=043804&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= MI5 &RL=1080*1920&OS=7.0&API=24
        Q-GUID: ed3467186e1125bb3d28234d13b788cb
        Q-Auth: 31045b957cf33acf31e40be2f3e71c5217597676a9729f1b
                """

        headers = utils.str_to_dict(headers)

        data_url = "https://mp.weixin.qq.com/mp/getappmsgext"

        r = requests.post(data_url, data=data, verify=False, params=data_url_params, headers=headers)

        result = r.json()
        if result.get("appmsgstat"):
            post['read_num'] = result.get("appmsgstat").get("read_num")
            post['like_num'] = result.get("appmsgstat").get("like_num")
            post['reward_num'] = result.get("reward_total_count")
            post['u_date'] = datetime.now()
            logger.info("「%s」read_num: %s like_num: %s reward_num: %s" %
                        (post.title, post['read_num'], post['like_num'], post['reward_num']))
            post.save()
        else:
            logger.warning(u"没有获取的真实数据，请检查请求参数是否正确，返回的数据为：data=%s" % r.text)
            exit()

if __name__ == '__main__':
    # 直接运行这份代码很定或报错，或者根本抓不到数据
    # 因为header里面的cookie信息已经过去，还有URL中的appmsg_token也已经过期
    # 你需要配合Fiddler或者charles通过手机重新加载微信公众号的更多历史消息
    # 从中获取最新的headers和appmsg_token替换上面
    crawler = WeiXinCrawler()
    # crawler.crawl()
    # s = "__biz=MjM5MzgyODQxMQ==&appmsg_type=9&mid=2650367540&sn=ef9c6353a9255dbc00e2beac7f449dad&idx=1&scene=27&title=Python%E5%A5%87%E6%8A%80%E6%B7%AB%E5%B7%A7%EF%BC%8C%E7%9C%8B%E7%9C%8B%E4%BD%A0%E7%9F%A5%E9%81%93%E5%87%A0%E4%B8%AA&ct=1511410410&abtest_cookie=AwABAAoADAANAAcAJIgeAGSIHgD8iB4A7IkeAAaKHgAPih4AU4oeAAAA&devicetype=android-24&version=/mmbizwap/zh_CN/htmledition/js/appmsg/index3a9713.js&f=json&r=0.04959653583814139&is_need_ad=0&comment_id=1411699821&is_need_reward=1&both_ad=0&reward_uin_count=24&msg_daily_idx=1&is_original=0&uin=777&key=777&pass_ticket=zpU4AwNXTGS5LfBXFx4NCyMo5YTpSQo9RarrPG3tjhmMaGfORzykNNviX7IlM4i0&wxtoken=1922467438&devicetype=android-24&clientversion=26051732&appmsg_token=938_0n0in1TAhMHhtZ7zXIOyxTxYXZEFW7ez7tXTmochNzKXa19P3wxK6-C-yM1omM_h7gSMZJmyv7glw98g&x5=1&f=json"
    # print(utils.str_to_dict(s, "&", "="))
    #
    for post in Post.objects(reward_num=0):
        crawler.update_post(post)
        time.sleep(1)
