#coding=utf-8
__author__ = 'sixkery'

import time
import base64
import json
from PIL import Image
from selenium import webdriver

def input_message():
    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8') # 设置中文格式
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('https://www.zhihu.com/signup?next=%2F') # 登录页面

    log_in_page = browser.find_elements_by_xpath('//div[@class="SignContainer-switch"]/span')[0]
    log_in_page.click()
    username = browser.find_elements_by_name('username')[0] # 获取用户的 input 标签
    time.sleep(1)
    username.send_keys('15937557924')
    password = browser.find_elements_by_name('password')[0] # 获取密码的 input 标签
    password.send_keys('1326628437g5')
    time.sleep(2)
    return browser

def handle_base64(new_img_code):
    # 处理经过 base64 加密的图片并保存到本地
    new_img_code = base64.b64decode(new_img_code)
    with open('img_code.jpg','wb') as f:
        f.write(new_img_code)


def show_img():
    # 把保存的图片展现出来
    img = Image.open('img_code.jpg')
    img.show()

def get_title(browser):
    # 获取登录后的的标题，证明登录成功
    title_list = browser.find_elements_by_xpath('//div[contains(@class, "TopstoryItem-isRecommend")]/div[@class="Feed"]/div[contains(@class, "AnswerItem")]')
    for title in title_list:
        title = title.get_attribute('data-zop')
        title = json.loads(title)
        print(title)

def main():

    while True:
        browser = input_message()
        # 查找英文验证码的标签
        lable_by_eng = browser.find_elements_by_xpath('//div[contains(@class, SignFlow-captchaContainer)]/div/span[@class="Captcha-englishImage"]')
        # 登录按钮
        button = browser.find_elements_by_xpath('//button[contains(@class, "SignFlow-submitButton")]')[0]
        if len(lable_by_eng) == 0:
            img_lable = browser.find_elements_by_xpath('//img[@class="Captcha-chineseImg"]')[0]  # 查找中文验证码标签
            img_url = img_lable.get_attribute('src')  # 验证码图片路径
            if img_url == 'data:image/jpg;base64,null':  # 判断是否有验证码
                print('没有验证码,直接点击登录！')
                button.click()
                time.sleep(3)
                get_title(browser)
                break
            else:
                print('中文验证码，暂时处理不了，跳过')
                continue
        elif len(lable_by_eng) == 1:
            img_lable = browser.find_elements_by_xpath('//img[@class="Captcha-englishImg"]')[0]  # 查找中文验证码标签
            img_url = img_lable.get_attribute('src')  # 验证码图片路径
            if img_url == 'data:image/jpg;base64,null':  # 判断是否有验证码
                print('没有验证码,直接点击登录！')
                button.click()
                time.sleep(3)
                get_title(browser)
                break
            else:
                base64_img_url = img_url.replace('data:image/jpg;base64,', '')  # 对base64做处理
                make_base64(base64_img_url)
                input_lable = browser.find_elements_by_name('captcha')[0]
                # show_img()
                # input_lable = input('手动打码，请输入验证码>>>')
                code = use_ydm('img_code.png')  # 调用云打码接口，返回识别后的内容
                input_lable.send_keys(code)  # 将验证码写入
                time.sleep(3)
                button.click()
                time.sleep(3)
                get_title(browser)  # 获取主页标题
                break


if __name__ == '__main__':
    main()
