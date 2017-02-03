# -*- coding: utf-8 -*-
import scrapy

from javhd.items import JavhdItem


class JavhdAllSpider(scrapy.Spider):
	name = "javhd_all"
	allowed_domains = []
	# start_urls = ['http://javhd.com/ja/models/']
	start_urls = ['http://javhd.com/zh/models']


	def parse(self, response):
		print("RESPONSE URL: {}".format(response.url))
		yield scrapy.Request("http://javhd.com/ja/models", headers={'Referer': response.url}, callback=self.parseJALang)


	def parseJALang(self, response):
		for i, div in enumerate(response.xpath("""//div[@class="thumbs4 models_items"]/div""")):
			print(i, div, div.xpath("./a/@href").extract_first(), div.xpath("./*/img/@src").extract_first(), div.xpath("""./*/span[@class="thumb-text"]/text()""").extract_first())
			item = {}
			item['response_url'] = response.url
			item['title'] = div.xpath("""./*/span[@class="thumb-text"]/text()""").extract_first()
			item['thumbnail_url'] = div.xpath("./*/img/@src").extract_first()
			item['image_urls'] = [item['thumbnail_url']]
			item['article_url'] = div.xpath("./a/@href").extract_first()
			item['articles'] = yield scrapy.Request(item['article_url'], meta={'item': item}, headers={'Referer': item['response_url']}, callback=self.scrape_articleContents)

		print(response.xpath("""./a[@class="next navi paging"]/@href""").extract_first())
		return None

	def scrape_articleContents(self, response):
		print(response.url)
		print(response.xpath("""//div[@class="model"]/a/img/@src""").extract_first())
		for li in response.xpath("""//div[@class="model"]/ul/li"""):
			print("----------	{}		{}".format(li.xpath("./span/text()").extract_first(), li.xpath("./text()").extract_first()))
		for tag in response.xpath("""//div[@class="modelinfo"]/p/*"""):
			print(tag)
		print(response.xpath("""//div[@class="modelinfo"]/p/text()""").extract_first().strip())