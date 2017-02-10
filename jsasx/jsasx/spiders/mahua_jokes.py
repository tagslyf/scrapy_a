# -*- coding: utf-8 -*-
import pprint, requests, scrapy

from jsasx.items import JsasxItem
from jsasx.settings import API_BASE_URL


class MahuaJokesSpider(scrapy.Spider):
	name = "mahua_jokes"
	allowed_domains = ["www.mahua.com"]
	start_urls = ['http://www.mahua.com/tags/7755_1.htm']

	def parse(self, response):
		dls = response.xpath("""//div[@class="left"]/dl""")
		for dl in dls:
			item = JsasxItem()
			item['categories'] = ["笑肖肖神回复"]
			item['title'] = dl.xpath("""./dt/span//text()""").extract_first()
			item['response_url'] = response.url
			img_tag = dl.xpath("""./dd[@class="content"]/img""")
			item['thumbnail_url'] = img_tag.xpath("@src").extract_first() if img_tag.xpath("@src").extract_first() else img_tag.xpath("@mahuaimg").extract_first()
			item['article_url'] = dl.xpath("""./dt/span/a/@href""").extract_first()
			search_response = requests.get("{}posts?search={}".format(API_BASE_URL, item['title']))
			if search_response.status_code == 200:
				if search_response.json():
					for post in search_response.json():
						if item['title'].strip() == post['title']['rendered'].strip():
							print("{}   {}  {}".format("Title existed in API.", item['article_url'], item['title']))
							continue
			item['articles'] = yield scrapy.Request(item['article_url'], meta={'item': item}, callback=self.parse_content)
		next_page = response.xpath("""//div/a[contains(text(), "下一页")]""").xpath("@href").extract_first()
		if next_page is not None:
			yield scrapy.Request(next_page, callback=self.parse)


	def parse_content(self, response):
		item = response.meta['item']
		item['articles'] = []
		item['image_urls'] = []
		item['image_only'] = False
		for content in response.xpath("""//dd[@class="content"]"""):
			if content.xpath(".//img"):
				item['articles'].append(content.xpath(".//img/@src").extract_first())
				item['image_urls'].append(content.xpath(".//img/@src").extract_first())
				item['image_only'] = True
			elif content.xpath("./*/text()"):
				item['articles'].extend([t.strip() for t in content.xpath("./*/text()").extract()])
		yield item
