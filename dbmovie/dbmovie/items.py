# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DbmovieItem(scrapy.Item):

    pass

class movie87Item(scrapy.Item):
    pic = scrapy.Field()#图片
    name = scrapy.Field()#原名

    type = scrapy.Field() # 类型

    content = scrapy.Field() #内容

    nickname = scrapy.Field()#别名
    score = scrapy.Field()#评分
    director = scrapy.Field()#导演
    scriptwriter = scrapy.Field() #编剧
    protagonist = scrapy.Field()#主演
    time = scrapy.Field()#年代
    showtime = scrapy.Field()#上映
    language = scrapy.Field()#语言
    length_of_a_film = scrapy.Field()#片长
    country = scrapy.Field()#国家
    synopsis = scrapy.Field()#剧情简介
    download_url = scrapy.Field()#下载链接


class dbmovieItem(scrapy.Item):
    pic = scrapy.Field()  # 图片
    name = scrapy.Field()  # 原名
    content = scrapy.Field()  # 内容
    synopsis = scrapy.Field()  # 剧情简介
    type = scrapy.Field()

    nickname = scrapy.Field() # 又名
    score = scrapy.Field()  # 评分
    director = scrapy.Field()  # 导演
    scriptwriter = scrapy.Field()  # 编剧
    protagonist = scrapy.Field()  # 主演
    time = scrapy.Field()  # 年代

    showtime = scrapy.Field()  # 上映
    language = scrapy.Field()  # 语言
    length_of_a_film = scrapy.Field()  # 片长
    country = scrapy.Field()  # 国家


