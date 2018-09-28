# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FashionnovaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dress_name = scrapy.Field()
    price = scrapy.Field()
    material_1 = scrapy.Field()
    material_2 = scrapy.Field()
    dress_img_1 = scrapy.Field()
    dress_img_2 = scrapy.Field()
