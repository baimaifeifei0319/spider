#coding=utf-8
__author__ = 'sixkery'

import html


def sub_dict(d,keys):
    '''工具函数，用于提取指定字段的内容'''
    return {k: html.unescape(d[k]) for k in d if k in keys}


def str_to_dict(s, join_symbol="\n", split_symbol=":"):
    """
    key与value通过split_symbol连接， key,value 对之间使用join_symbol连接
    例如： a=b&c=d   join_symbol是&, split_symbol是=
    :param s: 原字符串
    :param join_symbol: 连接符
    :param split_symbol: 分隔符
    :return: 字典
    """
    s_list = s.split(join_symbol)
    data = dict()
    for item in s_list:
        item = item.strip()
        if item:
            k, v = item.split(split_symbol, 1)
            data[k] = v.strip()
    return data

if __name__ == '__main__':

    d = {"a": "1", "b": '2', "c": '3'}
    print(sub_dict(d, ["a", "b"]))