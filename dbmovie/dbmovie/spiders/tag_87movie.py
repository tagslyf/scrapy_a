# -*- coding: utf-8 -*-
import scrapy
from ..items import movie87Item
import re
import urllib

class movie87_spider(scrapy.Spider):
    name = "tags_87movie"
    category = "热门电影"
    allowed_domains = ["87movie.com"]
    start_urls = ["http://www.87movie.com/"]
    # start_urls = ["http://www.87movie.com/tag/%E5%86%92%E9%99%A9/9?o=data"]

    def parse_item(self, response):
        movie87_one = response.meta['movie87_one']
        tag = response.meta['tag']
        movie87_one['pic'] = "http://" + response.url.split('/')[2] + \
                             response.xpath('//div[@class="thumbnail"]/img/@src').extract()[0]

        movie87_one['name'] = response.xpath('//div[@class="col-md-8"]/h3/text()').extract()
        movie87_one['type'] = tag
        movie87_one['content'] = response.xpath('//div[@class="col-md-8"]').extract()

        try:
            div_content = response.xpath('//div[@class="col-md-8"]').extract()[0]
        except:
            div_content = ""
        #
        # movie87_one['nickname'] = re.search("<strong>又名：</strong>(.*?)<br>", div_content).group(1)
        # movie87_one['score'] = response.xpath('//div[@class="col-md-8"]/span/text()').extract()[0]
        #
        # movie87_one['director'] = re.search("<strong>导演：</strong>(.*?)<br>", div_content).group(1)
        # movie87_one['director'] = re.search("<strong>编剧：</strong>(.*?)<br>", div_content).group(1)
        # movie87_one['protagonist'] = re.search("<strong>主演：</strong>(.*?)<br>", div_content).group(1)
        # movie87_one['time'] = re.search("<strong>影片年代：</strong>(.*?)<br>", div_content).group(1)
        # movie87_one['showtime'] = re.search("<strong>上映时间：</strong>(.*?)<br>", div_content).group(1)
        # movie87_one['language'] = re.search("<strong>语言：</strong>(.*?)<br>", div_content).group(1)
        # movie87_one['length_of_a_film'] = re.search("<strong>片长：</strong>(.*?)<br>", div_content).group(1)
        # movie87_one['country'] = re.search("<strong>国家：</strong>(.*?)<br>", div_content).group(1)
        try:
            movie87_one['synopsis'] = re.search("<strong>剧情简介：</strong>(.*?)<br>", div_content, re.S).group(1)
        except:
            movie87_one['synopsis'] = ""
        movie87_one['download_url'] = response.xpath('//div[@class="panel panel-default"]').extract()
        yield movie87_one

    def parse_page(self, response):
        tag = response.meta['tag']
        movies = response.xpath('//h4/a/@href').extract()
        url_host = 'http://'+response.url.split('/')[2]
        for i in movies:
            movie87_one = movie87Item()
            yield scrapy.Request(url_host + i, meta={'movie87_one': movie87_one, "tag":tag}, callback=self.parse_item)


    def parse_num(self, response):
        num_page = response.xpath('//ul[@class="pagination"]//li[last()]/a/@href').extract()
        tag = urllib.parse.unquote(response.url.split('/')[-1])
        number = 1
        if len(num_page) > 0:
            number = int(num_page[0].split('/')[-1].split('?')[0])
        for i in range(number):
            yield scrapy.Request(response.url +'/'+ str(i) + '?o=data', meta={'tag': tag}, callback=self.parse_page)

    def parse(self, response):
        tag_movies = response.xpath('//ul[@class="list-inline tags"]//li/a/@href').extract()
        url_host = "http://" + response.url.split('/')[2]
        for i in tag_movies:
            yield scrapy.Request(url_host+i, callback=self.parse_num)