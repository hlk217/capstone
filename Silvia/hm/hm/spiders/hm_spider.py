from scrapy import Spider, Request
from hm.items import HmItem

class HmSpider(Spider):
	name = "hm_spider"
	allowed_urls = ["http://www2.hm.com/en_us/index.html"]
	start_urls = ['http://www2.hm.com/en_us/women/products/dresses.html']

	def parse(self,response):
		allurls = ['http://www2.hm.com/en_us/women/products/dresses.html?product-type=ladies_dresses%2Cladies_dresses&sort=stock&offset=0&page-size=1020']
		for r in allurls: 
			yield Request(url = r, callback = self.parse_all_urls)


	def parse_all_urls(self,response):
		urls = response.xpath('//h3[@class="product-item-heading"]/a/@href').extract()
		newurls = map(lambda x:"http://www2.hm.com" + x,urls)

		for url in newurls:
			yield Request(url=url, callback = self.parse_result_page)

	def parse_result_page(self,response):
		#cmpurl = response.xpath('//div[@class="cmp_title"]/a/@href').extract()
		#print cmpurl
		#fullcmpurl = map(lambda x: "https://www.indeed.com" + x, cmpurl)
		#print fullcmpurl
		#print "=" * 50
		title = response.xpath('//h1[@class="primary product-item-headline"]/text()').extract_first()
		price = response.xpath('//span[@class="price-value"]/text()').extract_first()
		description = response.xpath('//p[@class="pdp-description-text"]/text()').extract_first()
		material = response.xpath('//div[@class="pdp-description-list"]/ul/li/text()').extract_first() 
		imgurl = response.xpath('//div[@class="product-detail-main-image-container"]/img/@src').extract()
		imgurls = map(lambda x:"https:" + x, imgurl)
		print(imgurls)

		item = HmItem()
		item['title'] = title
		item['price'] = price
		item['description'] = description
		item['material'] = material
		item['imgurl'] = imgurls
		

		yield item 