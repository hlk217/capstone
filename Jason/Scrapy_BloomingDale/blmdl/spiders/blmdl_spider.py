from scrapy import Spider, Request
from blmdl.items import BlmdlItem
import re
import numpy as np
import urllib.request 
import urllib.error
import os.path

class BlmdlSpider(Spider):
	name = 'blmdl_spider'
	allowed_urls = ['https://www.bloomingdales.com/']
	start_urls = ['https://www.bloomingdales.com/shop/womens-apparel/tops-tees/Pageindex,Productsperpage/1,96?id=5619']

	def parse(self, response):


		pagelist_urls = ["https://www.bloomingdales.com/shop/womens-apparel/tops-tees/Pageindex,Productsperpage/{},96?id=5619".format(i) for i in range(1, 6)]

		# Loop all the different product pages
		for url in pagelist_urls:
			print('#'*50)
			print(url)
			print('#'*50)

		#  Look into a particular page	
			yield Request(url = url, callback = self.parse_product_page)

	def parse_product_page(self, response):
		
		# Collect all the products into a list
		products = response.xpath('//li[@class="small-6 medium-4 large-3 columns"]')

		# Loop into the list to see the information of each product
		for product in products:
			# Get the link to the detailed page for a single item. 
			url_product = product.xpath('.//a[@class="productDescLink"]/@href').extract_first()
			price_reg = product.xpath('.//div[@class="productDetail"]//span[@class="regular"]/text()').extract_first().strip()

			# If there is a discount price then use it. If not just use the regular price. 
			if product.xpath('.//div[@class="productDetail"]//span[@class="discount"]/text()').extract_first() != None:
				price_dis = product.xpath('.//div[@class="productDetail"]//span[@class="discount"]/text()').extract_first().split()[1]
			else:
				price_dis = price_reg
			
			# Carry the price information into the next level. 
			# Get into the detailed product page. 
			yield Request(url = "https://www.bloomingdales.com"+url_product, meta={'price_reg':price_reg, 'price_dis':price_dis}, callback = self.parse_detail_page)

	def parse_detail_page(self, response):

		# Grab different information of a product
		brand = response.xpath('//h1/a[@id="brandNameLink"]/text()').extract_first()
		prod_name = response.xpath('//div[@id="productName"]/text()').extract_first()
		desc_list = response.xpath('//ul[@class="product-details-bullet-list"]/li/text()').extract()
		prod_image = response.xpath('//img[@itemprop="image"]/@src').extract_first()
		prod_img_full = prod_image+'?wid=1200&qlt=90,0&layer=comp&op_sharpen=0&resMode=sharp2&op_usm=0.7,1.0,0.5,0&fmt=jpeg'

		# Received the price information from the upper level. 
		price_reg = response.meta['price_reg']
		price_dis = response.meta['price_dis']
		print('#'*50)
		print(prod_image)
		print('#'*50)

		# This is for extracting product image################################		
		if prod_image != '':
			try:
				full_file_name =  'img' + re.split("\/", prod_image)[-1].replace('.','_')
				if ( not os.path.exists(full_file_name)):
					urllib.request.urlretrieve(prod_img_full,full_file_name) #download img
			except urllib.error.HTTPError as err:
				if err.code == 404:
					pass
				else:
					raise
		######################################################################



		item = BlmdlItem()
		item['brand'] = brand
		item['prod_name'] = prod_name
		item['price_reg'] = price_reg
		item['price_dis'] = price_dis
		item['desc_list'] = desc_list
		item['prod_image'] = prod_image
		item['full_file_name'] = full_file_name

		yield item

	