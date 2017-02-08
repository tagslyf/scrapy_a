# -*- coding: utf-8 -*-
import scrapy
from ..items import dbmovieItem
import re

class db_spider(scrapy.Spider):
    name = "later_douban"
    category = "即将上映"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/later/beijing/"]
    # start_urls = ["https://movie.douban.com/subject/26691509/",]

    def parse_item(self, response):
        # def parse(self, response):
        # later_movie = dbmovieItem()
        later_movie = response.meta['later_movie']

        later_movie['content'] = response.xpath('//div[@id="info"]').extract()
        # div_content = response.xpath('//div[@id="info"]').extract()[0]
        # print(div_content)

        later_movie['pic'] = response.xpath('//div[@id="mainpic"]/a/img/@src').extract()[0]
        later_movie['name'] = response.xpath('//div[@id="content"]/h1/span[@property="v:itemreviewed"]/text()').extract()
        # try:
        #     later_movie['nickname'] = re.search('<span class="pl">又名:</span>(.*?)<br>',div_content).group(1)
        # except:
        #     later_movie['nickname'] = []
        try:
            later_movie['score'] = response.xpath(
                '//div[@id="interest_sectl"]//strong[@class="ll rating_num"]/text()').extract()
        except:
            later_movie['score'] = []

        later_movie['type'] = response.xpath('//span[@property="v:genre"]/text()').extract()

        later_movie['synopsis'] = response.xpath('//div[@id="link-report"]/span/text()').extract()
        yield later_movie



    def parse(self, response):
        later_movies = response.xpath('//div[@class="tab-bd"]//div[@class="intro"]/h3/a/@href').extract()
        # print(later_movies,len(later_movies))


        for i in later_movies:
            later_movie = dbmovieItem()
            yield scrapy.Request(i, meta={'later_movie': later_movie}, callback=self.parse_item)