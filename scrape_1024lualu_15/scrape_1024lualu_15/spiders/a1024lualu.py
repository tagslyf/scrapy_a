# -*- coding: utf-8 -*-
import os, pprint, requests, scrapy, time
from bs4 import BeautifulSoup
from datetime import datetime

from scrape_1024lualu_15.items import Scrape1024Lualu15Item
from scrape_1024lualu_15.settings import API_BASE_URL


class A1024lualuSpider(scrapy.Spider):
	name = "1024lualu"
	allowed_domains = ["x3.1024lualu.pw"]
	start_urls = ['http://x3.1024lualu.pw/pw/thread.php?fid=15']

	# pages = 200
	pages = 1


	def parse(self, response):	
		for page in range(self.pages + 1)[::1]:
			if page:
				yield scrapy.Request("{}&page={}".format(self.start_urls[0], page), callback=self.parse_thread)


	def parse_thread(self, response):
		item = Scrape1024Lualu15Item()
		item['response_url'] = "http://x3.1024lualu.pw/pw/thread.php?fid=15"
		item['title'] = "丝袜制服美腿内射（29P）"
		item['thumbnail_url'] = ""
		item['article_url'] = "http://x3.1024lualu.pw/pw/htm_data/15/1702/545691.html"
		item['articles'] = yield scrapy.Request(item['article_url'], meta={'item': item}, callback=self.parse_threadDetail)
		return None
		for tr in response.xpath("""//table[@id="ajaxtable"]/tbody/tr[@align="center"]"""):
			if tr.xpath("./td/h3/a/text()").extract_first():
				item = Scrape1024Lualu15Item()
				item['response_url'] = response.url
				item['title'] = tr.xpath("./td/h3/a/text()").extract_first()[8:]
				item['thumbnail_url'] = ""
				item['article_url'] = "http://{}/pw/{}".format(self.allowed_domains[0], tr.xpath("./td/h3/a/@href").extract_first())
				search_response = requests.get("{}posts?search={}".format(API_BASE_URL, item['title']))
				if search_response.status_code == 200:
					if search_response.json():
						print("{}	{}	{}".format("Title existed in API.", item['article_url'], item['title']))
						continue
				item['articles'] = yield scrapy.Request(item['article_url'], meta={'item': item}, callback=self.parse_threadDetail)


	def parse_threadDetail(self, response):
		item = response.meta['item']
		item['image_urls'] = []
		item['articles'] = []
		if response.xpath("""//div[@id="read_tpc"]/img"""):
			for img in response.xpath("""//div[@id="read_tpc"]/img"""):
				if img.xpath("""./@src""").extract_first()[:4] == "http":
					item['articles'].append(img.xpath("""./@src""").extract_first())
					item['image_urls'].append(img.xpath("""./@src""").extract_first())
		else:
			html = BeautifulSoup(response.body, "html.parser")

			imgs = html.find('div', {'id': "read_tpc"}).findAll("img")
			for img in imgs:
				if img['src'][:4] == "http":
					item['articles'].append(img['src'])
					item['image_urls'].append(img['src'])
		yield item