# -*- coding: utf-8 -*-
import pprint, requests, scrapy

from jsasx.items import JsasxItem
from jsasx.settings import API_BASE_URL


class MahuaImagesSpider(scrapy.Spider):
	name = "mahua_images"
	allowed_domains = ["www.mahua.com"]
	start_urls = ['http://www.mahua.com/']

	def parse(self, response):
		dls = response.xpath("""//div[@class="left"]/dl""")
		for dl in dls:
			item = JsasxItem()
			item['title'] = dl.xpath("""./dt/span//text()""").extract_first()
			item['response_url'] = response.url
			img_tag = dl.xpath("""./dd[@class="content"]/img""")
			item['thumbnail_url'] = img_tag.xpath("@src").extract_first() if img_tag.xpath("@src").extract_first() else img_tag.xpath("@mahuaimg").extract_first()
			item['article_url'] = dl.xpath("""./dt/span/a/@href""").extract_first()
			search_response = requests.get("{}posts?search={}".format(API_BASE_URL, item['title']))
			if search_response.status_code == 200:
				if search_response.json():
					print("{}   {}  {}".format("Title existed in API.", item['article_url'], item['title']))
					continue
			item['articles'] = yield scrapy.Request(item['article_url'], meta={'item': item}, callback=self.parse_content)
		next_page = response.xpath("""//div[@class="page"]/a""")[-1].xpath("@href").extract_first()
		if next_page is not None:
			yield scrapy.Request(next_page, callback=self.parse)


	def parse_content(self, response):
		item = response.meta['item']
		item['articles'] = response.xpath("""//dd[@class="content"]//img/@src""").extract()
		item['image_urls'] = response.xpath("""//dd[@class="content"]//img/@src""").extract()
		item['image_only'] = True
		yield item
