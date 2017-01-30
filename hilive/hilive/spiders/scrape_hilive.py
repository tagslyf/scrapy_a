# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

from hilive.items import HiliveItem
from hilive.settings import DEFAULT_REQUEST_HEADERS


class ScrapeHiliveSpider(scrapy.Spider):
	name = "scrape_hilive"
	allowed_domains = ["www.hilive.tv"]
	start_urls = ['https://www.hilive.tv/NewsList/ALL?p=11']


	def parse(self, response):
		html = BeautifulSoup(response.body, "html.parser")

		for newsblock in html.findAll('div', {'class': "newsblock"}):
			news = HiliveItem()
			news['title'] = newsblock.find("h2").find("a").string
			news['response_url'] = response.url
			news['thumbnail_url'] = "https://{}{}".format(self.allowed_domains[0], newsblock.find("img")['src'])
			news['image_urls'] = []
			news['image_urls'].append("https://{}{}".format(self.allowed_domains[0], newsblock.find("img")['src']))
			news['article_url'] = "https://{}{}".format(self.allowed_domains[0], newsblock.find("h2").find("a")['href'])
			news['articles'] = yield scrapy.Request(news['article_url'], meta={'news': news}, callback=self.scrape_hiliveArticle)

		if html.find('a', {'id': "NextPage"}) and 'href' in html.find('a', {'id': "NextPage"}):
			yield scrapy.Request("https://{}{}".format(self.allowed_domains[0], html.find('a', {'id': "NextPage"})['href']), self.parse)


	def scrape_hiliveArticle(self, response):
		news = response.meta['news']
		news['articles'] = []
		html = BeautifulSoup(response.body, "html.parser")

		for d in html.find('div', {'class': "bodytxt"}).findAll("div"):
			if d.string:
				if d.string.strip():
					news['articles'].append(d.string.strip())
			elif d.find('img'):
				news['articles'].append(d.find("img")['src'])
				if d.find("img")['src'] not in news['image_urls']:
					news['image_urls'].append(d.find("img")['src'])
			else:
				article_string = " ".join([s.strip() for s in d.findAll(text=True)])
				remove = ["http://www.", "https://www.", "https://twitter.com/", "https://www.facebook.com/", "資料參考"]
				for w in remove:
					if w in article_string:
						article_string = ""
						break

				if article_string:
					news['articles'].append(article_string)

		yield news