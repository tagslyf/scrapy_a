# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

from nianhua03.items import Nianhua03Item

class ScrapeNianhua03Spider(scrapy.Spider):
	name = "scrape_nianhua03"
	allowed_domains = ["wap.nianhua03.xyz"]
	start_urls = ['http://wap.nianhua03.xyz/news/articlelist/36.html']

	
	def parse(self, response):
		html = BeautifulSoup(response.body, "html.parser")

		print(response.url)
		ul = html.find("ul", {'class': "list1"})
		if ul:
			lis = ul.findAll("li")
			if lis:
				for li in lis:
					print(li.find("a").string, "http://wap.nianhua03.xyz/{}".format(li.find("a")['href']))
					item = Nianhua03Item()
					item['response_url'] = "response.url"
					item['title'] = li.find("a").string
					item['article_url'] = "http://wap.nianhua03.xyz/{}".format(li.find("a")['href'])
					item['articles'] = yield scrapy.Request(item['article_url'], meta={'item': item}, callback=self.scrape_nianhua03Article)

		next_page = html.find("div", {'id': "channelshow"}).find("a", text="下一页")['href']
		if next_page:
			yield scrapy.Request("http://wap.nianhua03.xyz/{}".format(next_page), self.parse)

	 
	def scrape_nianhua03Article(self, response):
		item = response.meta['item']
		html = BeautifulSoup(response.body, "html.parser")
		item['articles'] = []
		item['image_urls'] = []

		article = html.find("article")
		if article:
			tags = article.findAll()
			if tags:
				for tag in tags:
					if tag.find("img"):
						item['image_urls'].append(tag.find("img")['src'])
						item['articles'].append(tag.find("img"))
					else:
						if tag.extract():
							item['articles'].append(tag.extract())

		yield item