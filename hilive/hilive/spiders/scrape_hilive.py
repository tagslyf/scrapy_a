# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class ScrapeHiliveSpider(scrapy.Spider):
    name = "scrape_hilive"
    allowed_domains = ["www.hilive.tv"]
    start_urls = ['https://www.hilive.tv/NewsList/ALL?p=1']

    def parse(self, response):
        html = BeautifulSoup(response.body, "html.parser")

        print(response.url)
        print(len(html.findAll('div', {'class': "newsblock"})))
        for newsblock in html.findAll('div', {'class': "newsblock"}):
        	print(newsblock.find("h2").find("a").string)

        if html.find('a', {'id': "NextPage"}):
        	yield scrapy.Request("https://{}{}".format(self.allowed_domains[0], html.find('a', {'id': "NextPage"})['href']), self.parse)

