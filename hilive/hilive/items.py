# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class HiliveItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	name = "HiliveItem"
	title = Field()
	response_url = Field()
	thumbnail_url = Field()
	article_url = Field()
	articles = Field()
	image_urls = Field()
	images = Field()
	