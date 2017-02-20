# -*- coding: utf-8 -*-
import scrapy
from ..items import BgxwItem
import re
from lxml import etree
import requests
from bs4 import BeautifulSoup


def parse_article(url):
    res = requests.get(url)
    bsp = BeautifulSoup(res.content, 'lxml')
    # div[@class="article_content"]
    cu_content = bsp.find("div",{"class":"article_content"})
    center = cu_content.find("center")
    return str(cu_content).replace(str(center),"")

class mx_spider(scrapy.Spider):
    name = "mingxing_huabian"
    category = "明星"
    allowed_domains = ["www.huabian.com","site.6park.com"]
    start_urls = ["http://www.huabian.com/mingxing/", "http://site.6park.com/enter8/index.php?app=forum&act=list"]
    # start_urls = ["http://www.huabian.com/mingxing/20170124/157623.html"]
    ready_url = "http://www.huabian.com/mingxing/{}.html"

    # def parse_article(self, response):
    #     mx_it = response.meta['mx_it']
    #     mx_it['title'] = response.xpath('//div[@class="box_left"]/h1/text()').extract()
    #
    #     mx_it['content'] = response.xpath('//div[@class="article_content"]').extract()
    #
    #     yield mx_it

    def parse_page(self, response):
        mx_it = response.meta['mx_it']
        mx_it['title'] = response.xpath('//div[@class="box_left"]/h1/text()').extract()

        mx_it['content'] = response.xpath('//div[@class="article_content"]').extract()
        # print( mx_it['content'], '内容' * 10)
        center = response.xpath('//div[@class="article_content"]/center').extract()
        # print(center,'广告'*10)
        try:
            mx_it['content'][0] = mx_it['content'][0].replace(center[0],"")
            # print("替换输出"*100)
        except:
            pass

        # print(mx_it['content'], '内容' * 10)

        many_links = response.xpath('//div[@id="show_pages"]/a/@href').extract()

        if len(many_links)>0:
            many_numbers = response.xpath('//div[@id="show_pages"]/a/text()').extract()
            # print(many_links, many_numbers, '*' * 100)
            try:
                max_numbers = many_numbers[-2]
            except:
                max_numbers = 0
            tag = response.url.split('/')[-1].replace('.html','')
            # mx_it['tag'] = tag
            cu_num = response.url
            cu_num = cu_num.replace('.html','')
            print('cu_num', cu_num, '*'*100)

            for i in range(2, int(max_numbers)+1):
                url = cu_num + '_' + str(i) + '.html'
                cu_content = parse_article(url)
                mx_it['content'][0] = mx_it['content'][0] + "<!--nextpage-->" + cu_content
        return mx_it


    def parse_link(self, response):
        all_links = response.xpath('//div[@class="newsList"]/ul//li//div[@class="title"]/a/@href').extract()
        for i in all_links:
            mx_it = BgxwItem()
            # if all_links.index(i)<1:
            #     yield scrapy.Request(i, meta={'mx_it': mx_it}, callback=self.parse_page)
            yield scrapy.Request(i, meta={'mx_it': mx_it}, callback=self.parse_page)


    def park_article(self, response):
        mx_it = response.meta['mx_it']
        mx_it['title'] = response.xpath('//td[@class="show_content"]/center/font/b/text()').extract()
        mx_it['content'] = response.xpath('//td[@class="show_content"]/pre').extract()
        yield mx_it

    def parse(self, response):
        if response.url == "http://www.huabian.com/mingxing/":
            pass
            # part one
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
        if response.url == "http://site.6park.com/enter8/index.php?app=forum&act=list":
            # part two
            # return None
            host_url = "http://site.6park.com/enter8/"
            mx_links = response.xpath('//li/a[text()="========== 中港台版 ========== (无内容)"]/../ul/li/a/@href').extract()
            for i in mx_links:
                mx_it = BgxwItem()
                yield scrapy.Request(host_url+i, meta={'mx_it': mx_it}, callback=self.park_article)