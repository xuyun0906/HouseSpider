# -*- coding: utf-8 -*-
import scrapy
import json
from items import XiaoquItem, XiaoquDetailItem, ZSHouseItem


class LianjiaSpiderSpider(scrapy.Spider):
    name = 'Lianjia_spider'
    allowed_domains = ['https://bj.lianjia.com/xiaoqu/']
    start_urls = ['https://bj.lianjia.com/xiaoqu/']

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse_region, dont_filter=True)

    def parse_region(self, response):
            dists = response.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
            for dist in dists:
                if dist.find("https") != -1:
                    url = dist
                else:
                    url = 'https://bj.lianjia.com' + dist
                yield scrapy.Request(url, self.parse_xiaoqu, dont_filter=True)

    def parse_xiaoqu(self, response):
        page_info = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
        page_dic = json.loads(page_info)
        page_num = page_dic.get('totalPage')
        for i in range(int(page_num)):
            url = response.url + 'pg' + str(i+1) + '/'
            yield scrapy.Request(url, callback=self.parse_xq_list, dont_filter=True)

    def parse_xq_list(self, response):
      xq_list = response.xpath("//ul[@class='listContent']/li")
      for xq in xq_list:
           item = XiaoquItem()
           xq_name = xq.xpath('.//div[@class="title"]/a/text()').extract()
           xq_url = xq.xpath('.//div[@class="title"]/a/@href').extract()
           item['id'] = xq_url
           item['name'] = xq_name
           sale_url = xq.xpath('.//a[@class="totalSellCount"]/@href').extract()
           houseInfo = xq.xpath('.//div[@class="houseInfo"]/a/text()').extract()
           if len(houseInfo) == 3:
             item['huxingCount'] = houseInfo[0]
             item['chengjiaoCount'] = houseInfo[1]
             item['zaizuCount'] = houseInfo[2]
           else :
             item['chengjiaoCount'] = houseInfo[0]
             item['zaizuCount'] = houseInfo[1]

           item['region'] = xq.xpath('.//div[@class="positionInfo"]/a[@class="district"]/text()').extract()
           item['district'] = xq.xpath('.//div[@class="positionInfo"]/a[@class="bizcircle"]/text()').extract()
           item['avgPrice'] = xq.xpath('.//div[@class="totalPrice"]/span/text()').extract()
           item['zaishouCount'] = xq.xpath('.//a[@class="totalSellCount"]/span/text()').extract()
           item['city'] = str("北京")
           yield scrapy.Request(xq_url, callback=self.parse_xq_detail, dont_filter=True)
           yield scrapy.Request(sale_url, callback=self.parse_house, dont_filter=True)
           yield item

     def parse_xq_detail(self, response):
        item = XiaoquDetailItem()
        item['id'] = response.url
        item['name'] = response.xpath('/html/body/div[4]/div/div[1]/h1').extract()
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
       page_info = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
       page_dic = json.loads(page_info)
       page_num = page_dic.get('totalPage')
       prefix = "https://bj.lianjia.com/ershoufang/"
       urlGroup = response.url.split(prefix)
       for i in range(int(page_num)):
          url = prefix + 'pg' + str(i + 1) + urlGroup[1]
         yield scrapy.Request(url, callback=self.parse_house_list, dont_filter=True)

    def parse_house_list(self, response):
      house_list = response.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGCLICKDATA"]')
      for house in house_list:
        item = ZSHouseItem()
        item['name'] = house.xpath('.//div[@class="title"]/a/text()').extract()
        item['city'] = str("北京")
        item['xiaoquId'] = house.xpath('//*[@id="sem_card"]/div/div[2]/div[1]/a[1]/@href').extract()
        item['xiaoquName'] = house.xpath('//*[@id="sem_card"]/div/div[2]/div[1]/a[1]/text()').extract()
        content = house.xpath('.//div[@class="address"]/div[@class="houseInfo"]').extract()
        if len(content):
            content = content[0].split('/')
            item['huXing'] = content[1]
            item['mianJi'] = content[2]
            item['direct'] = content[3]
            item['fitment'] = content[4]
            item['lift'] = content[5]

        content = house.xpath('.//div[@class="flood"]/div[@class="positionInfo"]').extract()
        if len(content):
           content = content[0].split('/')
           item['floor'] = content[0]
           item['buildType'] = content[1]
           item['district'] = content[2]

        item['totalPrice'] = house.xpath('.//div[@class="followInfo"]/div[@class="priceInfo"]/div[@class="totalPrice"]').extract()
        item['price'] = house.xpath('.//div[@class="followInfo"]/div[@class="priceInfo"]/div[@class="unitPrice"]').extract()
        yield  item
