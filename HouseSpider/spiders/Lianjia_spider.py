# -*- coding: utf-8 -*-
import json

import scrapy

from HouseSpider.items import XiaoquItem, XiaoquDetailItem, ZSHouseItem


class LianjiaSpiderSpider(scrapy.Spider):
    name = 'Lianjia_spider'
    allowed_domains = ['bj.lianjia.com']
    start_urls = ['https://bj.lianjia.com/xiaoqu/']
    city_url = 'https://bj.lianjia.com/city/'

    def start_requests(self):
        yield scrapy.Request(self.city_url, callback=self.parse_city, dont_filter=False)
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, callback=self.parse_region, dont_filter=False)

    def parse_city(self, response):
        citys_dic = {}
        citys = response.xpath('//div[@class="city_province"]//a')
        for city in citys:
            city_name = city.xpath('text()').extract()[0].strip()
            city_start = city.xpath('@href').extract()[0].strip().split('.')[0]
            citys_dic[city_start] = city_name
        self.citys_dic = citys_dic

    def parse_region(self, response):
        dists = response.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        for dist in dists:
            if dist.find("https") != -1:
                url = dist
            else:
                url = 'https://bj.lianjia.com' + dist
            yield scrapy.Request(url, self.parse_xiaoqu, dont_filter=False)

    def parse_xiaoqu(self, response):
        page_info = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
        page_dic = json.loads(page_info)
        page_num = page_dic.get('totalPage')
        for i in range(1, int(page_num) + 1):
            url = response.url + 'pg' + str(i + 1) + '/'
            yield scrapy.Request(url, callback=self.parse_xq_list, dont_filter=False)

    def parse_xq_list(self, response):
        xq_list = response.xpath("//ul[@class='listContent']/li")
        for xq in xq_list:
            item = XiaoquItem()
            xq_name = xq.xpath('.//div[@class="title"]/a/text()').extract()[0]
            xq_url = xq.xpath('.//div[@class="title"]/a/@href').extract()[0]
            item['id'] = xq_url.split('/')[-2]
            item['url'] = xq_url
            item['name'] = xq_name
            sale_url = xq.xpath('.//a[@class="totalSellCount"]/@href').extract()[0]
            houseInfo = xq.xpath('.//div[@class="houseInfo"]/a/text()').extract()
            if len(houseInfo) == 3:
                item['huxingCount'] = houseInfo[0]
                item['chengjiaoCount'] = houseInfo[1]
                item['zaizuCount'] = houseInfo[2]
            else:
                item['chengjiaoCount'] = houseInfo[0]
                item['zaizuCount'] = houseInfo[1]

            item['region'] = xq.xpath('.//div[@class="positionInfo"]/a[@class="district"]/text()').extract()[0]
            item['district'] = xq.xpath('.//div[@class="positionInfo"]/a[@class="bizcircle"]/text()').extract()[0]
            item['avgPrice'] = xq.xpath('.//div[@class="totalPrice"]/span/text()').extract()[0]
            item['zaishouCount'] = xq.xpath('.//a[@class="totalSellCount"]/span/text()').extract()[0]
            city_start = xq_url.split('.')[0]
            item['city'] = self.citys_dic[city_start]
            yield item
            yield scrapy.Request(xq_url, callback=self.parse_xq_detail, dont_filter=False)
            yield scrapy.Request(sale_url, callback=self.parse_house, dont_filter=False)


    def parse_xq_detail(self, response):
        item = XiaoquDetailItem()
        item['id'] = response.url.split('/')[-2]
        item['url'] = response.url
        item['name'] = response.xpath('/html/body/div[4]/div/div[1]/h1/text()').extract()[0]
        xq_detail = response.xpath('.//span[@class="xiaoquInfoContent"]/text()').extract()
        item['buildYear'] = xq_detail[0]
        item['bulidType'] = xq_detail[1]
        item['wuyeFee'] = xq_detail[2]
        item['wuyeCompany'] = xq_detail[3]
        item['developers'] = xq_detail[4]
        item['loudongCount'] = xq_detail[5]
        item['fangwuCount'] = xq_detail[6]
        yield item

    def parse_house(self, response):
        if '没有找到相关房源，您可以浏览我们为您推荐的房源' not in response.text:
            page_info = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
        else:
            page_info = json.dumps({'totalPage': 0})
        page_dic = json.loads(page_info)
        page_num = page_dic.get('totalPage')
        for i in range(1, int(page_num) + 1):
            url = response.url.replace('/c', '/pg{}c'.format(i))
            yield scrapy.Request(url, callback=self.parse_house_list, dont_filter=False)

    def parse_house_list(self, response):
        house_list = response.xpath('//li[@class="clear LOGCLICKDATA"]')
        for house in house_list:
            item = ZSHouseItem()
            item['url'] = response.url
            item['name'] = house.xpath('div[@class="info clear"]/div[@class="title"]/a/text()').extract()[0]
            city_start = response.url.split('.')[0]
            item['city'] = self.citys_dic[city_start]
            item['xiaoquId'] = response.url.split('c')[-1][:-1]
            # item['xiaoquName'] = house.xpath('//*[@id="sem_card"]/div/div[2]/div[1]/a[1]/text()')
            address_content = house.xpath('div[@class="info clear"]/div[@class="address"]').xpath('string(.)').extract()[0]
            if len(address_content):
                address_content = address_content.split('/')
                for key, value in zip(['xiaoquName', 'huXing', 'mianJi', 'direct', 'fitment', 'lift'], address_content):
                    item[key] = value

            positionInfo_content = house.xpath('div[@class="info clear"]/div[@class="flood"]').xpath('string(.)').extract()[0]
            if len(positionInfo_content):
                positionInfo_content = positionInfo_content.split('/')
                item['floor'] = positionInfo_content[0]
                item['buildType'] = positionInfo_content[1]
                item['district'] = positionInfo_content[2]
            item['totalPrice'] = house.xpath('div[@class="info clear"]/div[@class="followInfo"]/div[@class="priceInfo"]/div[@class="totalPrice"]').xpath('string(.)').extract()[0]

            item['price'] = house.xpath('div[@class="info clear"]/div[@class="followInfo"]/div[@class="priceInfo"]/div[@class="unitPrice"]').xpath('string(.)').extract()[0]
            yield item
