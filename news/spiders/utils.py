#coding=utf-8
__date__ = ' 20:47'
__author__ = 'sixkery'

import hashlib

def get_md5(content):
    return hashlib.md5(content.encode()).hexdigest()