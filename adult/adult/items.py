# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class AdultItem(Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	name = "AdultItem"
	thread_url = Field()
	topic_id = Field()
	topic_title = Field()
	topic_url = Field()
	image_urls = Field()
	images = Field()