# -*- coding: utf-8 -*-
import pprint, scrapy

from sxsbz.items import SxsbzItem, ContentItem


class Lashu8AllSpider(scrapy.Spider):
	name = "lashu8_all"
	allowed_domains = ["www.lashu8.com"]
	start_urls = ['http://www.lashu8.com/']

	def parse(self, response):
		top_novels = response.xpath("""//div[@class="m1l"]/ul/li""")
		category = "<em><strong>{}</strong></em>".format(response.xpath("""//div[@class="m1l"]/h2/span/text()""").extract_first())
		for novel in top_novels:
			item = SxsbzItem()
			item['response_url'] = response.url
			item['title'] = novel.xpath("""./a""")[1].xpath("""./text()""").extract_first()
			item['thumbnail_url'] = "http://{}{}".format(self.allowed_domains[0], novel.xpath("""./a""")[0].xpath("""./img/@src""").extract_first())
			item['article_url'] = "http://{}{}".format(self.allowed_domains[0], novel.xpath("""./a""")[1].xpath("""./@href""").extract_first())
			item['articles'] = [category]
			yield scrapy.Request(item['article_url'], meta={'item': item}, callback=self.parse_article)
			
			break
		yield item


	def parse_article(self, response):
		item = response.meta['item']
		chapters = response.xpath("""//div[@class="mulu"]/ul/li""")
		chapters_dict = {}
		for index, chapter in enumerate(chapters):
			chapter_url = "http://{}{}".format(self.allowed_domains[0], chapter.xpath("""./a/@href""").extract_first())
			chapters_dict[str(index)] = ContentItem()
			chapters_dict[str(index)]['chapter'] = ["<br><strong>{}</strong>".format(" ".join(chapter.xpath("""./a//text()""").extract()))]
			chapters_dict[str(index)]['contents'] = []
			yield scrapy.Request(chapter_url, meta={'data': chapters_dict, 'index': str(index)}, callback=self.parse_chapter)
			break
		print("XXXX", chapters_dict)
		for index, key in enumerate(chapters_dict):
			print(index)
			print(chapters_dict[str(index)]['chapter'])
			print(chapters_dict[str(index)]['contents'])
			item['articles'].extend(chapters_dict[str(index)]['chapter'])
			item['articles'].extend(chapters_dict[str(index)]['contents'])

		return item


	def parse_chapter(self, response):
		data = response.meta['data']
		index = response.meta['index']
		data[index]['contents'].extend(response.xpath("""//div[@class="mcc"]//text()""").extract())

		return data