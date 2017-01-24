# -*- coding: utf-8 -*-
import scrapy


class Scrape1024lualuSpider(scrapy.Spider):
    name = "scrape_1024lualu"
    allowed_domains = ["x3.1024lualu.pw"]
    start_urls = ['http://x3.1024lualu.pw/pw/thread.php?fid=16']

    def parse(self, response):
        pass
