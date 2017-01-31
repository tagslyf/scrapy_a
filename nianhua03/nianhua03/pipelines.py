# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os, requests, scrapy
from scrapy.pipelines.images import ImagesPipeline
from nianhua03.settings import UPLOAD_API_TOKEN, IMAGES_STORE


class Nianhua03Pipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):
		image_paths = [(x['path'], x['url']) for ok, x in results if ok]

		api_base_url = "http://jpavnews.com/wp-json/wp/v2/"
		content = ""
		for image_path, image_url in image_paths:
			headers = {}
			headers['Authorization'] = "Bearer {}".format(UPLOAD_API_TOKEN)
			headers['Content-Disposition'] = "attachment;filename={}".format(image_path.split("/")[-1])
			file = open("{}/{}".format(IMAGES_STORE, image_path), "rb")
			filename = image_path.split("/")[-1]
			files = {
				'file': (filename, file, 'image/{}'.format(filename.split(".")[-1]))
			}
			thumbnail_url = tuple()
			try:
				response = requests.post("{}{}".format(api_base_url, "media"), headers=headers, files=files)
			except Exception as ex:
				pass
			else:
				if image_url in item['articles']:
					item_index = item['articles'].index(image_url)
					item['articles'][item_index] = """
						<img src='{}'>
					""".format(response.json()['source_url'])
				elif image_url == item['thumbnail_url']:
					thumbnail_url = (response.json()['id'], response.json()['source_url'])
			file.close()
			os.remove("{}/{}".format(IMAGES_STORE, image_path))

		headers = {'Authorization': "Bearer {}".format(UPLOAD_API_TOKEN)}
		data = {
			'title': item['title'],
			'content': "<br> ".join(item['articles']),
			'status': 'publish',
			'categories': [1]
		}
		try:
			response = requests.post("{}{}".format(api_base_url, "posts"), headers=headers, data=data)
		except Exception as ex:
			pass
		else:
			print("Success uploading to API.")

		return item