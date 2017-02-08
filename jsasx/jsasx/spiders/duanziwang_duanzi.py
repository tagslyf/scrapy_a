# -*- coding: utf-8 -*-
import requests, scrapy

from jsasx.items import JsasxItem
from jsasx.settings import API_BASE_URL


class DuanziwangDuanziSpider(scrapy.Spider):
	name = "duanziwang_duanzi"
	allowed_domains = ["duanziwang.com"]
	start_urls = ['http://duanziwang.com/category/duanzi']

	def parse(self, response):
		articles = response.xpath("""//div[@class="content"]/article""")
		for article in articles:
			item = JsasxItem()
			title = article.xpath("""./header/h2//text()""").extract_first()
			item['title'] = title
			item['response_url'] = response.url
			item['thumbnail_url'] = ""
			item['article_url'] = article.xpath("""./header/h2/a/@href""").extract_first()
			search_response = requests.get("{}posts?search={}".format(API_BASE_URL, item['title']))
			if search_response.status_code == 200:
				if search_response.json():
					print("{}   {}  {}".format("Title existed in API.", item['article_url'], item['title']))
					continue
			item['articles'] = yield scrapy.Request(item['article_url'], meta={'item': item}, callback=self.parse_content)
		next_page = response.xpath("""//li[@class="next-page"]/a/@href""").extract_first()
		if next_page is not None:
			yield scrapy.Request(next_page, callback=self.parse)


	def parse_content(self, response):
		item = response.meta['item']
		item['articles'] = response.xpath("""//article[@class="article-content"]/p/text()""").extract()
		item['image_urls'] = []
		item['image_only'] = False
		yield item