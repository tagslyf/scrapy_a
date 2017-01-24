# -*- coding: utf-8 -*-
import requests, scrapy
from adult.items import AdultItem
from bs4 import BeautifulSoup


class Scrape1024lualuSpider(scrapy.Spider):
	name = "scrape_1024lualu"
	allowed_domains = ["x3.1024lualu.pw"]
	start_urls = ['http://x3.1024lualu.pw/pw/thread.php?fid=16']

	def parse(self, response):
		html = BeautifulSoup(response.body, "html.parser")

		if html.find('table', {'id': "ajaxtable"}):
			table = html.find('table', {'id': "ajaxtable"})
			if table.find('tbody', {'style': "table-layout:fixed;"}):
				tbody = table.find('tbody', {'style': "table-layout:fixed;"})

				for tr in tbody.findAll("tr"):
					try:
						if tr.findAll("td")[1].img is None:
							if tr.findAll("td")[1].h3.a.string:
								tds = tr.findAll("td")
								thread = AdultItem()
								thread['title'] = tds[1].h3.a.string
								thread['content_url'] = "http://{}/pw/{}".format(self.allowed_domains[0], tds[1].h3.a['href'])
								thread['thread_id'] = tds[1].h3.a.get('id')
								thread['content_images'] = []
								response = requests.get(thread['content_url'])
								print(response.status_code)
								if response.status_code == 200:
									html = BeautifulSoup(response.content, "html.parser")

									if html.find('div', {'id': "read_tpc"}):
										content = html.find('div', {'id': "read_tpc"})

										imgs = content.findAll('img')
										for img in imgs:
											thread['content_images'].append(img['src'])
								yield thread
					except Exception as ex:
						pass