from scrapy import Spider, Request
from fashionnova.items import FashionnovaItem
import urllib.request
import urllib.error
import os.path
import re

class FashionNovaSpider(Spider):
    name = 'fashionnova_spider'
    allowed_urls = ['https://www.fashionnova.com/']
    start_urls = ['https://www.fashionnova.com/collections/basic-top-test']

    def parse(self, response):
        result_urls = ['https://www.fashionnova.com/collections/basic-top-test?page={}'.format(x) for x in range(1,5)]
        for url in result_urls:
            yield Request(url = url, callback = self.parse_page)

    def parse_page(self, response):

        sites = response.xpath('//div[@id="collection"]/div/div/form/div/a/@href').extract()
        official_sites = ['https://www.fashionnova.com/{}'.format(x) for x in sites]

        for site in official_sites:
            yield Request(url = site, callback = self.parse_info)

    def parse_info(self, response):
        dress_name = response.xpath('.//div/h1[@class="title large--left small--left"]/text()').extract()
        price =  response.xpath('//section[@id="product-info"]/form/div/div/meta/@content').extract()[-1]
        material_1 = response.xpath('.//div/div[@class="group-body"]/ul/li/text()').extract()[-1]
        material_2 = response.xpath('.//div/div[@class="group-body"]/ul/li/text()').extract()[-2]
        dress_img_link = response.xpath('//div[@id="product-wrap"]/div/div/div/div/div/a/@href').extract()
        dress_img_list_1 = ['https:{}'.format(x) for x in dress_img_link][0] #download img
        dress_img_list_2 = ['https:{}'.format(x) for x in dress_img_link][1]

        print('='*50)

        #dress_img_1_name = os.getcwd() + '/img_top/' + re.split("\/", dress_img_list_1)[-1] + '.jpg'
        #urllib.request.urlretrieve(dress_img_list_1, dress_img_1_name)



        item = FashionnovaItem()
        item['dress_name'] = dress_name
        item['price'] = price
        item['material_1'] = material_1
        item['material_2'] = material_2
        item['dress_img_1'] = dress_img_list_1
        item['dress_img_2'] = dress_img_list_2
        yield item
