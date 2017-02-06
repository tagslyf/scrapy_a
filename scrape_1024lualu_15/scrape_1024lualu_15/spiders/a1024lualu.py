# -*- coding: utf-8 -*-
import scrapy
import os, pprint, requests, scrapy, time
from scrape_1024lualu_15.items import Scrape1024Lualu15Item
from bs4 import BeautifulSoup
from datetime import datetime


class A1024lualuSpider(scrapy.Spider):
	name = "1024lualu"
	allowed_domains = ["x3.1024lualu.pw"]
	start_urls = ['http://x3.1024lualu.pw/pw/thread.php?fid=15']

	page_num = 0

	def parse(self, response):
		print(response.xpath("""//div[@class="pages"]/a"""))
		print(response.xpath("""//div[@class="pages"]/a""").extract())
		print(response.xpath("""//div[@class="pages"]/a""").extract()[-1])


	def parse_thread(self, response):
		print()
