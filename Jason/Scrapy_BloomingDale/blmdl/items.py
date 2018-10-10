# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BlmdlItem(Item):
	brand = Field()
	prod_name = Field()
	price_reg = Field()
	price_dis = Field()
#	desc_list = Field()
#	prod_image = Field()
#	full_file_name = Field()