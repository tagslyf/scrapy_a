# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class ScrapeHiliveSpider(scrapy.Spider):
    name = "scrape_hilive"
    allowed_domains = ["www.hilive.tv"]
    start_urls = ['https://www.hilive.tv/NewsList/ALL?p=1']

    def parse(self, response):
        html = BeautifulSoup(response.body, "html.parser")

    print(response.url)
    print(len(html.findAll('div', {'class': "newsblock"})))
    for newsblock in html.findAll('div', {'class': "newsblock"}):
        news = {}
        news['title'] = newsblock.find("h2").find("a").string
        news['thumbnail_url'] = "{}{}".format(self.allowed_domains[0], newsblock.find("img")['src'])
        news['image_urls'] = []
        news['image_urls'].append("https://{}{}".format(self.allowed_domains[0], newsblock.find("img")['src']))
        news['article_url'] = "https://{}{}".format(self.allowed_domains[0], newsblock.find("h2").find("a")['href'])
        articles = yield scrapy.Request(news['article_url'], meta={'news': news}, callback=self.scrape_hiliveArticle)
        news['articles'] = articles
        yield news
        return None

    if html.find('a', {'id': "NextPage"}) and 'href' in html.find('a', {'id': "NextPage"}):
        yield scrapy.Request("https://{}{}".format(self.allowed_domains[0], html.find('a', {'id': "NextPage"})['href']), self.parse)


    def scrape_hiliveArticle(self, response):
        news = response.meta['news']
        news['articles'] = []
        html = BeautifulSoup(response.body, "html.parser")

        for d in html.find('div', {'class': "bodytxt"}).findAll("div"):
            print(d)
        return news