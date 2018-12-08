# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from settings import *
from items import XiaoquItem, XiaoquDetailItem, ZSHouseItem
import MySQLdb

class HousespiderPipeline(object):

    def open_spider(self, spider):
        self.con = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DBNAME, charset="utf8")
        self.cursor = self.con.cursor()


    def process_item(self, item, spider):

        if isinstance(item, XiaoquItem):
            insert_sql = "INSERT INTO xiaoqu_list(id, name, huxingCount, chengjiaoCount, zaizuCount, zaishouCount, avgPrice, region, district, city, buildYear) " \
                         "VALUES  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(insert_sql, (item['id'], item['name'], item['huxingCount'], item['chengjiaoCount'], item['zaizuCount'], item['zaishouCount'], item['avgPrice'],
                                             item['region'], item['district'], item['city'], item['buildYear']))
        elif isinstance(item, XiaoquDetailItem):
            insert_sql = "INSERT INTO xiaoqu_detail(id, name, buildYear, bulidType, wuyeFee, wuyeCompany, developers, loudongCount, fangwuCount) " \
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(insert_sql,(item['id'], item['name'], item['buildYear'], item['bulidType'], item['wuyeFee'], item['wuyeCompany'], item['developers'], item['loudongCount'], item['fangwuCount']))

        elif isinstance(item, ZSHouseItem):
            insert_sql = "INSERT INTO house_list(name, city, xiaoquId, xiaoquName, mianJi, floor, huXing, totalPrice, price, direct, fitment, lift, buildType, district) " \
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(insert_sql, (item['name'], item['city'], item['xiaoquId'], item['xiaoquName'], item['mianJi'], item['floor'],
            item['huXing'], item['totalPrice'], item['price'], item['direct'], item['fitment'], item['lift'],
            item['buildType'], item['district']))

        else:
            pass

        self.con.commit()
        return item


    def spider_close(self, spider):
        self.con.close()
