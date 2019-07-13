#coding=utf-8
__date__ = ' 9:01'
__author__ = 'sixkery'

#Redis数据库地址
REDIS_HOST = 'localhost'

#Redis数据库端口
REDIS_PORT = 6379

#Redis数据库密码
REDIS_PASSWORD = None

#有序集合键名
REDIS_KEY = 'proxies'

#代理分数
MAX_SCORE = 100#最大分数
MIN_SCORE = 0#最小分数
INITIAL_SCORE = 10#初始分数

#代理检测状态码
VALID_STATUS_CODES = [200,302]

#代理池数量界限
POOL_UPPER_THRESHOLD = 1000

#检查周期
TESTER_CYCLE = 20
#获取周期
GETTER_CYCLE = 300

#测试API，建议抓取那个网站测试那个网站
TEST_URL = 'http://weixin.sogou.com/weixin?type=2&query=读书'

#api配置
API_HOST = '0.0.0.0'
API_PORT = 5555

#开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

#批量测试最大量
BATCH_TEST_SIZE = 10
