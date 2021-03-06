# -*- coding: utf-8 -*-
import os, requests, scrapy
from bs4 import BeautifulSoup
from bs4.element import Tag

from hilive.items import HiliveItem
from hilive.settings import API_BASE_URL


class ScrapeHiliveSpider(scrapy.Spider):
	name = "scrape_hilive"
	allowed_domains = ["www.hilive.tv"]
	start_urls = ['https://www.hilive.tv/NewsList/ALL?p=1']

	posts = {}


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
			search_response = requests.get("{}posts?search={}".format(API_BASE_URL, news['title']))
			if search_response.status_code == 200:
				if search_response.json():
					print("{}	{}	{}".format("Title existed in API.", news['article_url'], news['title']))
					continue
			news['articles'] = yield scrapy.Request(news['article_url'], headers={'Referer': news['response_url']}, meta={'news': news}, callback=self.scrape_hiliveArticle)
		next_page = html.find('a', {'id': "NextPage"})['href']
		if next_page is not None:
			yield scrapy.Request("https://{}{}".format(self.allowed_domains[0], next_page), callback=self.parse)


	def scrape_hiliveArticle(self, response):
		news = response.meta['news']
		html = BeautifulSoup(response.body, "html.parser")

		news['articles'] = []
		for tag in html.find('div', {'class': "bodytxt"}):
			if tag.find("img"):
				if type(tag.find("img")) is Tag:
					news['image_urls'].append(tag.find("img")['src'])
					news['articles'].append(tag.find("img")['src'])
			elif tag.findAll(text=True):
				if len(" ".join([s.strip() for s in tag.findAll(text=True)]).strip()) > 0:
					remove_strings = ["https://twitter.com/imanaga_sana", "http://gazo.tokyo/archives/23821", "http://sumomo-ch.com/blog-entry-5032.html", "http://tengusan.com/archives/64440182.html", "://www.hi"]
					article_string = " ".join([s.strip() for s in tag.findAll(text=True)])
					for w in remove_strings:
						if w in article_string:
							article_string = ""
					article_string = article_string.replace("HiLive", "").replace("hilive", "")
					news['articles'].append(article_string)
		yield news