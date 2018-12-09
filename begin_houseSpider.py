#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/12 14:18
# @Author  : xuyun03
# @Site    : 
# @File    : begin_houseSpider.py
# @Software: PyCharm

from scrapy import cmdline

cmdline.execute('scrapy crawl Lianjia_spider'.split())
