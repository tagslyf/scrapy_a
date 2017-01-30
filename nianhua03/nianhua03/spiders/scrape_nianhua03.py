# -*- coding: utf-8 -*-
import scrapy


class ScrapeNianhua03Spider(scrapy.Spider):
    name = "scrape_nianhua03"
    allowed_domains = ["wap.nianhua03.xyz"]
    start_urls = ['http://wap.nianhua03.xyz/']

    def parse(self, response):
        pass
