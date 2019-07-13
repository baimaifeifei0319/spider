#coding=utf-8
__date__ = '2018/8/1 20:00'
__author__ = 'sixkery'

from api import app
from schedule import Schedule

def main():
    s = Schedule()
    s.run()
    app.run()

if __name__ == '__main__':
    main()