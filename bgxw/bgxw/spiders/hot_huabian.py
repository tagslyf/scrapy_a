# -*- coding: utf-8 -*-
import scrapy
from ..items import BgxwItem
import re
from .tuku_huabian import tubagua_spider
from .mingxing_huabian import mx_spider
import requests
from bs4 import BeautifulSoup



def parse_article(url):
    res = requests.get(url)
    bsp = BeautifulSoup(res.content, 'lxml')
    cu_content = bsp.find("div",{"class":"big-pic"})
    return str(cu_content)
def parse_article_mx(url):
    res = requests.get(url)
    bsp = BeautifulSoup(res.content, 'lxml')
    # div[@class="article_content"]
    cu_content = bsp.find("div",{"class":"article_content"})
    return str(cu_content)

class hot_spider(scrapy.Spider):
    name = "hot_huabian"
    category = "热点"
    allowed_domains = ["www.huabian.com","site.6park.com"]
    start_urls = ["http://www.huabian.com","http://site.6park.com/enter8/index.php?app=forum&act=list"]
    ready_url = "http://www.huabian.com/mingxing/{}.html"

    def parse_page_mx(self, response):
        mx_it = response.meta['mx_it']
        mx_it['title'] = response.xpath('//div[@class="box_left"]/h1/text()').extract()

        mx_it['content'] = response.xpath('//div[@class="article_content"]').extract()
        # print( mx_it['content'], '内容' * 10)
        center = response.xpath('//div[@class="article_content"]/center').extract()
        # print(center,'广告'*10)
        try:
            mx_it['content'][0] = mx_it['content'][0].replace(center[0], "")
            # print("替换输出"*100)
        except:
            pass

            # print(mx_it['content'], '内容' * 10)

        many_links = response.xpath('//div[@id="show_pages"]/a/@href').extract()

        if len(many_links) > 0:
            many_numbers = response.xpath('//div[@id="show_pages"]/a/text()').extract()
            # print(many_links, many_numbers, '*' * 100)
            try:
                max_numbers = many_numbers[-2]
            except:
                max_numbers = 0
            tag = response.url.split('/')[-1].replace('.html', '')
            # mx_it['tag'] = tag
            cu_num = response.url
            cu_num = cu_num.replace('.html', '')
            print('cu_num', cu_num, '*' * 100)

            for i in range(2, int(max_numbers) + 1):
                url = cu_num + '_' + str(i) + '.html'
                cu_content = parse_article_mx(url)
                mx_it['content'][0] = mx_it['content'][0] + "<!--nextpage-->" + cu_content

        return mx_it


    def parse_page_tk(self, response):
        mx_it = response.meta['mx_it']
        mx_it['title'] = response.xpath('//div[@class="box01"]/h1/text()').extract()
        mx_it['content'] = response.xpath('//div[@class="big-pic"]').extract()

        tag = response.url.split('/')[-1].replace('.html', '')
        # mx_it['tag'] = tag
        many_links = response.xpath('//div[@id="pages"]//a/@href').extract()

        if len(many_links) > 2:
            many_links.pop()
            many_links.remove(many_links[0])
            # many_links[0] = response.url
            for i in many_links:
                cu_content = parse_article(i)
                mx_it['content'][0] = mx_it['content'][0] + "<!--nextpage-->" + cu_content

        return mx_it

    def park_article(self, response):
        mx_it = response.meta['mx_it']
        mx_it['title'] = response.xpath('//td[@class="show_content"]/center/font/b/text()').extract()
        mx_it['content'] = response.xpath('//td[@class="show_content"]/pre').extract()
        # print(mx_it['title'])
        yield mx_it

    def parse(self, response):
        if response.url == "http://www.huabian.com":
            # part one
            top_links = response.xpath('//div[@class="list"]/ul//li/div/a/@href').extract()
            bottom_one_links = response.xpath('//div[@class="area-main mr10"]//a/@href').extract()
            bottom_one_links = list(set(bottom_one_links))
            print(len(top_links), len(bottom_one_links))
            mx_it = BgxwItem()
            for i in top_links:
                yield scrapy.Request(i, meta={'mx_it': mx_it}, callback=self.parse_page_tk)
            for i in bottom_one_links:
                yield scrapy.Request(i, meta={'mx_it': mx_it}, callback=self.parse_page_mx)

        if response.url == "http://site.6park.com/enter8/index.php?app=forum&act=list":
            # part two
            host_url = "http://site.6park.com/enter8/"
            park_hot = response.xpath('//div[@id="d_gold_list"]/table//td/a/@href').extract()
            print(park_hot, len(park_hot))
            for i in park_hot:
                mx_it = BgxwItem()
                # print(host_url+i)
                yield scrapy.Request(host_url+i, meta={'mx_it': mx_it}, callback=self.park_article)