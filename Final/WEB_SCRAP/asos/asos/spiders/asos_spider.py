from scrapy import Spider, Request
from asos.items import AsosItem
import re
import os.path
import urllib.request 


class AsosSpider(Spider):
	name = 'asos_spider'
	allowed_urls = ['http://us.asos.com/women/']
	start_urls = ['http://us.asos.com/women/dresses/cat/?cid=8799&nlid=ww|clothing|shop+by+product']

	def parse(self, response):
		# Find the total number of pages in the result so that we can decide how many urls to scrape next
		text = response.xpath('//p[@class="_2sxPqJf"]/text()').extract_first()
		per_page, total1, total2 = map(lambda x: int(x), re.findall('\d+', text))
		number_pages = round((total1*1000+total2)/per_page)

		# List comprehension to construct all the urls
		result_urls = ['http://us.asos.com/women/dresses/cat/?cid=8799&nlid=ww|clothing|shop%20by%20product&page={}'.format(x) for x in range(1, number_pages)]

		# Yield the requests to different search result urls, 
		# using parse_result_page function to parse the response.
		for url in result_urls:
			yield Request(url=url, callback=self.parse_result_page)


	def parse_result_page(self, response):
		# This fucntion parses the search result page.
		
		products = response.xpath('//a[@class="_3x-5VWa"]')
		
		for product in products:
			detail_url = product.xpath('.//@href').extract_first()  # We are looking for url of the detail page.
			price = product.xpath('.//p/span[2]/text()').extract_first()

		# Yield the requests to the details pages, 
		# using parse_detail_page function to parse the response.
		# carry the price down since price can't be scraped on item page
			yield Request(url=detail_url, meta={'price': price}, callback=self.parse_detail_page)



	def parse_detail_page(self, response):
		# This fucntion parses the product detail page.

		product = response.xpath('//div[@class="product-hero"]/h1/text()').extract_first()
		price = response.meta['price']
		description = response.xpath('//div[@class="product-description"]/span/ul/li/text()').extract()
		material = response.xpath('//div[@class="about-me"]/span//text()').extract()
		front_img = 'https:'+ response.xpath('//img/@src')[7].extract()						# front size image (already sized correctly)
		back_img = 'https:'+ response.xpath('//img/@src')[4].extract().split("?")[0]		# back side image (resized)
		
		# This is for extracting product image ################################		
		
		full_file_name_front = os.getcwd() + '/img_dress/' + re.split("\/", front_img)[-1] + '.jpg'		# file path/name
		urllib.request.urlretrieve(front_img, full_file_name_front)										# download front img
		
		full_file_name_back = os.getcwd() + '/img_dress/' + re.split("\/", back_img)[-1] + '.jpg'		# file path/name
		urllib.request.urlretrieve(back_img, full_file_name_back)										# download back img


		item = AsosItem()
		item['product'] = product
		item['price'] = price
		item['description'] = description
		item['material'] = material
		item['front_img'] = front_img
		item['back_img'] = back_img
		
		yield item




