import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from jsasx.spiders.duanziwang import DuanziwangSpider
from jsasx.spiders.duanziwang_duanzi import DuanziwangDuanziSpider
from jsasx.spiders.duanziwang_duanzilaile import DuanziwangDuanzilaileSpider
from jsasx.spiders.duanziwang_quotations import DuanziwangQuotationsSpider
from jsasx.spiders.mahua_images import MahuaImagesSpider
from jsasx.spiders.mahua_jokes import MahuaJokesSpider


if __name__ == "__main__":
	print("Hello world.")

	settings = get_project_settings()
	process = CrawlerProcess(settings)
	process.crawl(DuanziwangSpider)
	process.crawl(DuanziwangDuanziSpider)
	process.crawl(DuanziwangDuanzilaileSpider)
	process.crawl(DuanziwangQuotationsSpider)
	process.crawl(MahuaImagesSpider)	
	process.crawl(MahuaJokesSpider)
	process.start() # the script will block here until all crawling jobs are finished