# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class Nianhua03Item(scrapy.Item):
    # define the fields for your item here like:
    name = "Nianhua03Item"
    response_url = Field()
    title = Field()
    article_url = Field()
    articles = Field()
    image_urls = Field()
