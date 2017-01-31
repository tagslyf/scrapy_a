# -*- coding: utf-8 -*-
import logging, scrapy
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
					item['response_url'] = response.url
					item['title'] = li.find("a").string
					item['article_url'] = "http://wap.nianhua03.xyz/{}".format(li.find("a")['href'])
					item['articles'] = yield scrapy.Request(item['article_url'], meta={'item': item}, callback=self.scrape_nianhua03Article)

		next_page = html.find("div", {'id': "channelshow"}).find("a", text="下一页")['href']
		if next_page:
			return None
			yield scrapy.Request("http://wap.nianhua03.xyz/{}".format(next_page), self.parse)

	 
	def scrape_nianhua03Article(self, response):
		item = response.meta['item']
		html = BeautifulSoup(response.body, "html.parser")
		item['articles'] = []
		item['articles'].append(html.find("article").find("h1").string.strip())
		ais = html.find("article").find("div", {'class': "info"})
		article_info = []
		for ai in ais:
			if "getNewsHit" not in ai.string:
				article_info.append(ai.string)
		item['articles'].append(" ".join(article_info))
		item['image_urls'] = []

		article = html.find("div", {'class': "content"})
		if article:
			tags = article.findAll()
			if tags:
				for tag in tags:
					if tag.find("img"):
						item['image_urls'].append(tag.find("img")['src'])
						if tag.find("img") not in item['articles']:
							item['articles'].append(tag.find("img")['src'])
					else:
						if tag.extract():
							item['articles'].append(''.join(tag.findAll(text=True)))

		yield item