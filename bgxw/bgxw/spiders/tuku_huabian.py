# -*- coding: utf-8 -*-
import scrapy
from ..items import BgxwItem
import re
import requests
from lxml import etree
from bs4 import BeautifulSoup


def parse_article(url):
    res = requests.get(url)
    bsp = BeautifulSoup(res.content, 'lxml')
    cu_content = bsp.find("div",{"class":"big-pic"})
    return str(cu_content)

class tubagua_spider(scrapy.Spider):
    name = "tubagua_huabian"
    category = "图八卦"
    allowed_domains = ["www.huabian.com"]
    start_urls = ["http://www.huabian.com/tushuobagua/"]
    # start_urls = ["http://www.huabian.com/mingxing/20170124/157623.html"]
    ready_url = "http://www.huabian.com/tushuobagua/{}.html"

    def parse_page(self, response):
        mx_it = response.meta['mx_it']
        mx_it['title'] = response.xpath('//div[@class="box01"]/h1/text()').extract()
        mx_it['content'] = response.xpath('//div[@class="big-pic"]').extract()

        tag = response.url.split('/')[-1].replace('.html','')
        # mx_it['tag'] = tag
        many_links = response.xpath('//div[@id="pages"]//a/@href').extract()

        if len(many_links)>2:
            many_links.pop()
            many_links.remove(many_links[0])
            # many_links[0] = response.url
            for i in many_links:
                cu_content = parse_article(i)
                mx_it['content'][0] = mx_it['content'][0]+"<!--nextpage-->"+cu_content
        return mx_it



    def parse_link(self, response):
        all_links = response.xpath('//div[@id="container"]//div[@class="cell"]/a/@href').extract()
        for i in all_links:
            mx_it = BgxwItem()
            yield scrapy.Request(i, meta={'mx_it': mx_it}, callback=self.parse_page)



    def parse(self, response):
        all_page = response.xpath('//div[@id="pages"]//a/text()').extract()
        try:
            max_num = int(all_page[-2])
        except:
            max_num = 400
        for i in range(1, max_num+1):
            if i == 1:
                i = 'index'
                # request_url = self.ready_url.format(i)
                # yield scrapy.Request(request_url, callback=self.parse_link)
            request_url = self.ready_url.format(i)
            yield scrapy.Request(request_url, callback=self.parse_link)
        # yield scrapy.Request("http://www.huabian.com/mingxing/index.html", callback=self.parse_link)