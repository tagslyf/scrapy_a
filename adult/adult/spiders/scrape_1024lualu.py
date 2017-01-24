# -*- coding: utf-8 -*-
import os, pprint, requests, scrapy
from adult.items import AdultItem
from bs4 import BeautifulSoup


class Scrape1024lualuSpider(scrapy.Spider):
	name = "scrape_1024lualu"
	allowed_domains = ["x3.1024lualu.pw"]
	start_urls = ['http://x3.1024lualu.pw/pw/thread.php?fid=16']

	CONTENT_DIR = "adult/contents"
	folder_name = ""
	page_dir = ""
	thread_dir = ""


	def __init__(self):
		if not os.path.isdir(self.CONTENT_DIR):
			os.mkdir(self.CONTENT_DIR)

		if not os.path.isdir("{}/{}".format(self.CONTENT_DIR, self.name)):
			os.mkdir("{}/{}".format(self.CONTENT_DIR, self.name))

		self.folder_name = "{}/{}".format(self.CONTENT_DIR, self.name)


	def parse(self, response):
		html = BeautifulSoup(response.body, "html.parser")

		page_counter = int(html.find("div", {'class': "pages"}).findAll("a")[-1]['href'].split("=")[-1])

		for page_num in range(page_counter, 0, -1):
			url = "{}&page={}".format(self.start_urls[0], page_num)
			yield scrapy.Request(url, meta={'page_num': page_num}, callback=self.scrape_thread)
			


	def scrape_thread(self, response):

		page_num = response.meta['page_num']
		html = BeautifulSoup(response.body, "html.parser")

		if html.find('table', {'id': "ajaxtable"}):
			table = html.find('table', {'id': "ajaxtable"})
			if table.find('tbody', {'style': "table-layout:fixed;"}):
				tbody = table.find('tbody', {'style': "table-layout:fixed;"})
				if len(tbody.findAll("tr")) > 0:
					self.page_dir = "{}/{}".format(self.folder_name, page_num)
					if not os.path.isdir(self.page_dir):
						os.mkdir(self.page_dir)

					for tr in tbody.findAll("tr"):
						try:
							if tr.findAll("td")[1].img is None:
								if tr.findAll("td")[1].h3.a.string:
									tds = tr.findAll("td")
									thread = AdultItem()
									thread['title'] = tds[1].h3.a.string
									thread['content_url'] = "http://{}/pw/{}".format(self.allowed_domains[0], tds[1].h3.a['href'])
									thread['thread_id'] = tds[1].h3.a.get('id')
									yield scrapy.Request(thread['content_url'], meta={'item': thread}, callback=self.scrape_threadContent)
						except Exception as ex:
							pass


	def scrape_threadContent(self, response):
		thread = response.meta['item']
		thread['content_images'] = []
		html = BeautifulSoup(response.body, "html.parser")

		if html.find('div', {'id': "read_tpc"}):
			content = html.find('div', {'id': "read_tpc"})
			imgs = content.findAll('img')
			if len(imgs) > 0:
				self.thread_dir = "{}/{}".format(self.page_dir, thread['thread_id'].split("_")[-1])
				if not os.path.isdir(self.thread_dir):
					os.mkdir(self.thread_dir)

				for img in imgs:
					img_url = img['src']
					try:
						response = requests.get(img_url, timeout=60)
					except Exception as ex:
						pass
					else:
						if response.status_code == 200:
							filename = img_url.split("/")
							filename = filename[-1]
							with open("{}/{}".format(self.thread_dir, filename[:filename.index(".") + 4]), "wb") as f:
								for c in response:
									f.write(c)
						
						thread['content_images'].append({'url': img_url, 'path': "{}/{}".format(self.thread_dir, filename)})
				with open("{}/{}".format(self.thread_dir, "details.txt"), "w") as f:
					pprint.pprint(thread, f)
		return thread