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
			item = JavhdItem()
			item['response_url'] = response.url
			item['title'] = div.xpath("""./*/span[@class="thumb-text"]/text()""").extract_first()
			item['thumbnail_url'] = div.xpath("./*/img/@src").extract_first()
			item['image_urls'] = [item['thumbnail_url']]
			item['article_url'] = div.xpath("./a/@href").extract_first()
			item['articles'] = yield scrapy.Request(item['article_url'], meta={'item': item}, headers={'Referer': item['response_url']}, callback=self.scrape_articleContents)

		next_page = response.xpath("""//a[@class="next navi paging"]/@href""").extract_first()
		if next_page:
			yield scrapy.Request(next_page, self.parseJALang)

	def scrape_articleContents(self, response):
		item = response.meta['item']
		item['articles'] = [response.xpath("""//div[@class="model"]/a/img/@src""").extract_first()]
		item['image_urls'].append(response.xpath("""//div[@class="model"]/a/img/@src""").extract_first())
		for li in response.xpath("""//div[@class="model"]/ul/li"""):
			item['articles'].append("{}: {}".format(li.xpath("./span/text()").extract_first(), li.xpath("./text()").extract_first()))
		item['articles'].append(response.xpath("""//div[@class="modelinfo"]/p/b/text()""").extract_first().strip())
		item['articles'].append(response.xpath("""//div[@class="modelinfo"]/p/text()""").extract_first().strip())

		yield item