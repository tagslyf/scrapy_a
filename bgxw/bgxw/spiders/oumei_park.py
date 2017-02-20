# -*- coding: utf-8 -*-
import scrapy
from ..items import BgxwItem


class hot_spider(scrapy.Spider):
    name = "oumei_park"
    category = "欧美"
    allowed_domains = ["site.6park.com"]
    start_urls = ["http://site.6park.com/enter8/index.php?app=forum&act=list"]


    def park_article(self, response):
        mx_it = response.meta['mx_it']
        mx_it['title'] = response.xpath('//td[@class="show_content"]/center/font/b/text()').extract()
        mx_it['content'] = response.xpath('//td[@class="show_content"]/pre').extract()
        yield mx_it


    def parse(self, response):
        host_url = "http://site.6park.com/enter8/"
        mx_links = response.xpath('//li/a[text()="========== 欧美版 ========== (无内容)"]/../ul/li/a/@href').extract()
        for i in mx_links:
            mx_it = BgxwItem()
            yield scrapy.Request(host_url + i, meta={'mx_it': mx_it}, callback=self.park_article)
