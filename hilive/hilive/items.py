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
    news_title = Field()
    news_url = Field()
    news_thumbnail = Field()
    image_urls = Field()
    images = Field()
    article_url = Field()
    articles = Field()