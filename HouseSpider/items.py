# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy import Item, Field


class XiaoquItem(scrapy.Item):
    id = scrapy.Field()  # 小区ID
    url = scrapy.Field()  # 小区链接
    name = scrapy.Field()  # 小区名字
    huxingCount = scrapy.Field()  # 户型数
    chengjiaoCount = scrapy.Field()  # 历史成交套数
    zaizuCount = scrapy.Field()  # 在租套数
    zaishouCount = scrapy.Field()  # 在售套数
    avgPrice = scrapy.Field()  # 均价
    region = scrapy.Field()  # 区域
    district = scrapy.Field()  # 二级区域
    city = scrapy.Field()  # 城市


class XiaoquDetailItem(scrapy.Item):
    id = scrapy.Field()  # 小区ID
    url = scrapy.Field()  # 小区链接
    name = scrapy.Field()  # 小区名字
    buildYear = scrapy.Field()  # 建筑年代
    bulidType = scrapy.Field()  # 建筑类型
    wuyeFee = scrapy.Field()  # 物业费用
    wuyeCompany = scrapy.Field()  # 物业公司
    developers = scrapy.Field()  # 开发商
    loudongCount = scrapy.Field()  # 楼栋总数
    fangwuCount = scrapy.Field()  # 房屋总数


class ZSHouseItem(scrapy.Item):
    url = scrapy.Field()  # 房屋链接
    name = scrapy.Field()  # 房屋名称
    city = scrapy.Field()  # 城市
    xiaoquId = scrapy.Field()  # 小区ID
    xiaoquName = scrapy.Field()  # 小区名字
    mianJi = scrapy.Field()  # 面积
    floor = scrapy.Field()  # 楼层
    huXing = scrapy.Field()  # 户型
    totalPrice = scrapy.Field()  # 总价
    price = scrapy.Field()  # 单价
    direct = scrapy.Field()  # 朝向
    fitment = scrapy.Field()  # 装修
    lift = scrapy.Field()  # 电梯
    buildType = scrapy.Field()  # 建造类型
    district = scrapy.Field()  # 二级区域
