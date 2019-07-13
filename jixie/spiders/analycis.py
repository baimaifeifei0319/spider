#coding=utf-8
__date__ = ' 17:54'
__author__ = 'sixkery'

from pymongo import MongoClient
import jieba
import os,re
from wordcloud import WordCloud
from pyecharts import Pie
from pyecharts import Bar

class Analycis():
    def __init__(self):
        self.client = MongoClient(host='localhost',port=27017) # 连接本地数据库
        self.db = self.client['51JOB'] # 连接表
        self.collection = self.db['JixieItem'] # 指定集合

    def get_degree(self):
        # 获取学历要求
        content = ''
        degree = self.collection.find({},{'_id': False, 'degree': True})
        for i in degree:
            if '招' in i['degree'] or '人' in i['degree']:
                i['degree'] = '无学历要求'
            content += i['degree']

            undergraduate_num = content.count('本科') # 本科人数
            master_num = content.count('硕士') #硕士人数
            junior_num = content.count('大专') # 大专人数
            abc_num = content.count('无学历要求') #无学历要求人数
            attr = ['硕士','本科','大专','无学历要求']
            value = [master_num,undergraduate_num,junior_num,abc_num]
        return attr, value

    def get_describe(self):
        # 获取描述信息
        content = ''
        describe = self.collection.find({},{'_id': False, 'describe': True})
        for i in describe:
            content += i['describe']
        return content

    def get_experience(self):
        # 获取工作经验
        wt = ''
        experience = self.collection.find({},{'_id': False, 'experience': True})
        for i in experience:
            wt = wt+i['experience']
            experience1 = wt.count('无工作经验') #无工作经验人数
            experience2 = wt.count('1年经验')
            experience3 = wt.count('2年经验')
            experience4 = wt.count('3-4年经验')
            experience5 = wt.count('5-7年经验')
            experience6 = wt.count('8-9年经验')
            experience7 = wt.count('10年以上经验')
            attr = ['无工作经验', '1年经验', '2年经验', '3-4年经验','5-7年经验','8-9年经验','10年以上经验']
            value = [experience1,experience2,experience3,experience4,experience5,experience6,experience7]
        return attr,value


    def get_company_type(self):
        #获取公司类型
        wi = ''
        company_type = self.collection.find({},{'_id': False, 'company_type': True})
        for i in company_type:
            wi = wi+i['company_type']
            company_type1 = wi.count('民营公司')
            company_type2 = wi.count('外贸')
            company_type3 = wi.count('合资')
            company_type4 = wi.count('国企')
            company_type5 = wi.count('上市公司')
            attr = ['民营公司','外贸','合资','国企','上市公司']
            value = [company_type1,company_type2,company_type3,company_type4,company_type5]
        print(company_type1,company_type2,company_type3,company_type4,company_type5)
        return attr,value



    # 展示饼图
    def showPie(self):
        title = '           公司类型'
        attr,value = self.get_company_type()

        pie = Pie(title)
        # pie.add("aa", attr, value, is_label_show=True, title_pos='center')
        pie.add("",
                attr,
                value,
                radius=[40, 75],
                label_text_color=None,
                is_label_show=True,
                legend_orient="vertical",
                legend_pos="left", )
        pie.render('公司类型.html')

    def get_wordcloud(self):
        # 词云图
        content = self.get_describe()
        contents = jieba.lcut(content,cut_all=False)
        txt = ' '.join(contents)
        w = WordCloud(font_path='msyh.ttc',width=1000,max_font_size=100,font_step=2,
                      height=700,max_words=600,stopwords={'机械','span','br','工作','大专','经验','公司','设计','项目','产品',
                                                          'nbsp','indent','相关专业','div','family','text','style','font','岗位要求',
                                                          'li','任职资格','以上学历','有限公司','em','相关','宋体','任职要求',
                                                          '任职','要求','岗位职责','以上','优先','使用','能力','优先考虑','具有',
                                                          '合作','精神','团队','良好','以及','沟通'})
        w.generate(txt)
        w.to_file('机械词云图.jpg')

    def get_bar(self):
        # 展示柱状图
        attr, value = self.get_experience()
        bar = Bar('数据来源：','公众号sixkery')
        bar.add('经验分布',attr,value)
        bar.render()



if __name__ == '__main__':
    analycis = Analycis()
    analycis.get_wordcloud()
    # content = analycis.get_describe()
    # analycis.get_wordcloud(content)
    # # attr,value = analycis.get_degree()
    # # analycis.showPie('             ' + '学历分布',attr,value)
