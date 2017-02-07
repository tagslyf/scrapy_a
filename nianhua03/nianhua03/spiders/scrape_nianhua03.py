# -*- coding: utf-8 -*-
import requests, scrapy
from bs4 import BeautifulSoup

from nianhua03.items import Nianhua03Item
from nianhua03.settings import API_BASE_URL


class ScrapeNianhua03Spider(scrapy.Spider):
	name = "scrape_nianhua03"
	allowed_domains = ["wap.nianhua03.xyz"]
	start_urls = ['http://wap.nianhua03.xyz/news/articlelist/36.html']

	
	def parse(self, response):
		for li in response.xpath('//ul[@class="list1 pd10"]/li'):
			item = Nianhua03Item()
			item['response_url'] = response.url
			item['title'] = li.xpath('./a/text()').extract_first()
			item['article_url'] = "http://wap.nianhua03.xyz{}".format(li.xpath('./a/@href').extract_first())
			item['thumbnail_url'] = ""
			search_response = requests.get("{}posts?search={}".format(API_BASE_URL, item['title']))
			if search_response.status_code == 200:
				if search_response.json():
					print("{}	{}	{}".format("Title existed in API.", item['article_url'], item['title']))
					continue
			item['articles'] = yield scrapy.Request(item['article_url'], meta={'item': item}, headers={'Referer': item['response_url']}, callback=self.scrape_nianhua03Article)
		next_page = response.xpath('//div[@id="channelshow"]/a[contains(text(), "下一页")]/@href').extract_first()
		if next_page:
			yield scrapy.Request("http://wap.nianhua03.xyz{}".format(next_page), self.parse)


	def scrape_nianhua03Article(self, response):
		item = response.meta['item']
		item['articles'] = []
		item['image_urls'] = []
		item['articles'].append(response.xpath("//article/*")[0].xpath("./text()").extract_first())
		string_published = []
		for t in response.xpath("//article/*")[1].xpath("./*"):
			if t.xpath("name()").extract_first() in ["time"]:
				string_published.append(t.xpath("./text()").extract_first())
		item['articles'].append(" ".join(string_published))
		for t in response.xpath("//article/*")[2].xpath("./*"):
			if  t.xpath("./@src").extract_first():
				if not item['thumbnail_url']:
					item['thumbnail_url'] = t.xpath("./@src").extract_first()
				item['image_urls'].append(t.xpath("./@src").extract_first())
				item['articles'].append(t.xpath("./@src").extract_first())
			elif t.xpath(".//img").extract_first():
				if not item['thumbnail_url']:
					item['thumbnail_url'] = t.xpath(".//img/@src").extract_first()
				item['image_urls'].append(t.xpath(".//img/@src").extract_first())
				item['articles'].append(t.xpath(".//img/@src").extract_first())
			else:
				if t.xpath("./text()").extract_first():
					item['articles'].append(t.xpath("./text()").extract_first().strip())
		yield item