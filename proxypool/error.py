#coding=utf-8
__date__ = ' 10:18'
__author__ = 'sixkery'
class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已枯竭')