# -*- coding: utf-8 -*-
import scrapy
from ..items import movie87Item
import re

class movie87_spider(scrapy.Spider):
    name = "high_score_87movie"
    category = "本周高分榜"
    allowed_domains = ["87movie.com"]
    start_urls = ["http://www.87movie.com/"]

    def parse_item(self, response):
        movie87_one = response.meta['movie87_one']
        movie87_one['pic'] = "http://" + response.url.split('/')[2] + \
                             response.xpath('//div[@class="thumbnail"]/img/@src').extract()[0]

        movie87_one['name'] = response.xpath('//div[@class="col-md-8"]/h3/text()').extract()


        movie87_one['type'] = ""
        movie87_one['content'] = response.xpath('//div[@class="col-md-8"]').extract()

        # movie87_one['download_url'] = response.xpath('//div[@class="panel-body"]').extract()
        movie87_one['download_url'] = response.xpath('//div[@class="panel panel-default"]').extract()
        print(movie87_one['download_url'])
        try:
            div_content = response.xpath('//div[@class="col-md-8"]').extract()[0]
        except:
            div_content = ""
        # try:
        #     movie87_one['nickname'] = re.search("<strong>又名：</strong>(.*?)<br>", div_content).group(1)
        # except:
        #     movie87_one['nickname'] = ""
        # movie87_one['score'] = response.xpath('//div[@class="col-md-8"]/span/text()').extract()
        # try:
        #     movie87_one['director'] = re.search("<strong>导演：</strong>(.*?)<br>", div_content).group(1)
        # except:
        #     movie87_one['director'] = ""
        # movie87_one['scriptwriter'] = re.search("<strong>编剧：</strong>(.*?)<br>", div_content).group(1)
        # movie87_one['protagonist'] = re.search("<strong>主演：</strong>(.*?)<br>", div_content).group(1)
        # movie87_one['time'] = re.search("<strong>影片年代：</strong>(.*?)<br>", div_content).group(1)
        # movie87_one['showtime'] = re.search("<strong>上映时间：</strong>(.*?)<br>", div_content).group(1)
        # try:
        #     movie87_one['language'] = re.search("<strong>语言：</strong>(.*?)<br>", div_content).group(1)
        # except:
        #     movie87_one['language'] = ""
        # try:
        #     movie87_one['length_of_a_film'] = re.search("<strong>片长：</strong>(.*?)<br>", div_content).group(1)
        # except:
        #     movie87_one['length_of_a_film'] = ""
        # movie87_one['country'] = re.search("<strong>国家：</strong>(.*?)<br>", div_content).group(1)
        try:
            movie87_one['synopsis'] = re.search("<strong>剧情简介：</strong>(.*?)<br>", div_content, re.S).group(1)
        except:
            movie87_one['synopsis'] = ""

        yield movie87_one

    def parse(self, response):
        ten_movies = response.xpath('//div[@class="white-div"]//ol[@class="db-rank"]//li/a/@href').extract()
        # print(ten_movies)
        url_host = "http://" + response.url.split('/')[2]

        for i in ten_movies:
            # print("http://" + response.url.split('/')[2] + i)
            movie87_one = movie87Item()
            yield scrapy.Request(url_host+i, meta={'movie87_one': movie87_one}, callback=self.parse_item)
        # return None