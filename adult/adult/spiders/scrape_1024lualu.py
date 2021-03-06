# -*- coding: utf-8 -*-
import os, pprint, requests, scrapy
from adult.items import AdultItem
from bs4 import BeautifulSoup


class Scrape1024lualuSpider(scrapy.Spider):
	name = "scrape_1024lualu"
	allowed_domains = ["x3.1024lualu.pw"]
	start_urls = ['http://x3.1024lualu.pw/pw/thread.php?fid=16']

	CONTENT_DIR = "adult/contents"
	page_num = 0

	def __init__(self):
		pass


	def parse(self, response):
		html = BeautifulSoup(response.body, "html.parser")

		if not self.page_num:
			# self.page_num = int(html.find("div", {'class': "pages"}).findAll("a")[-1]['href'].split("=")[-1]) # Getting the last page
			self.page_num = 100 # Set 100 pages only
		
		while self.page_num > 0:
			url = "{}&page={}".format(self.start_urls[0], self.page_num)
			# print(url)
			if self.page_num:
				yield scrapy.Request(url, meta={'page_num': self.page_num}, callback=self.scrape_thread)
			self.page_num -= 1

	def scrape_thread(self, response):
		page_num = response.meta['page_num']
		html = BeautifulSoup(response.body, "html.parser")
		if html.find('table', {'id': "ajaxtable"}):
			table = html.find('table', {'id': "ajaxtable"})
			if table.find('tbody', {'style': "table-layout:fixed;"}):
				tbody = table.find('tbody', {'style': "table-layout:fixed;"})
				if len(tbody.findAll("tr")) > 0:
					for tr in tbody.findAll("tr"):
						try:
							if tr.findAll("td")[1].img is None:
								if tr.findAll("td")[1].h3.a.string:
									if "1024核工厂动态美图" in tr.findAll("td")[1].h3.a.string:
										continue
									tds = tr.findAll("td")
									thread = {}
									thread['thread_url'] = response.url
									thread['topic_title'] = tds[1].h3.a.string[8:]
									thread['topic_url'] = "http://{}/pw/{}".format(self.allowed_domains[0], tds[1].h3.a['href'])
									thread['topic_id'] = tds[1].h3.a.get('id')
									yield scrapy.Request(thread['topic_url'], meta={'item': thread}, callback=self.scrape_threadContent)
						except Exception as ex:
							pass


	def scrape_threadContent(self, response):
		thread = response.meta['item']
		html = BeautifulSoup(response.body, "html.parser")

		if html.find('div', {'id': "read_tpc"}):
			content = html.find('div', {'id': "read_tpc"})
			thread['image_urls'] = [img['src'] for img in content.findAll('img')] if len(content.findAll('img')) > 0 else []

			item = AdultItem(
				thread_url=thread['thread_url'],
				topic_id=thread['topic_id'], 
				topic_title=thread['topic_title'],
				topic_url=thread['topic_url'],
				image_urls=thread['image_urls']
			)
			yield item