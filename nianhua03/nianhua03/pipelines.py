# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os, requests, scrapy
from scrapy.pipelines.images import ImagesPipeline
from nianhua03.settings import API_BASE_URL, CATEGORY_LIST, IMAGES_STORE, MEDIA_URL, MEDIA_API_TOKEN, UPLOAD_API_TOKEN


class Nianhua03Pipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):
		if item['articles']:
			for image in item['images']:
				if image['url'] == item['thumbnail_url']:
					headers = {
						'Referer': item['response_url']
					}
					response = requests.get(image['url'], headers=headers)
					with open("downloads/{}".format(image['path']), "wb") as f:
						for c in response:
							f.write(c)
					break

			image_paths = [(x['path'], x['url']) for ok, x in results if ok]

			image_ids = []
			thumbnail_url = tuple()
			content = ""
			for image_path, image_url in image_paths:
				headers = {}
				headers['Content-Disposition'] = "attachment;filename={}".format(image_path.split("/")[-1])
				file = open("{}/{}".format(IMAGES_STORE, image_path), "rb")
				filename = image_path.split("/")[-1]
				files = {
					'file': (filename, file, 'image/{}'.format(filename.split(".")[-1]))
				}
				try:
					if image_url == item['thumbnail_url']:
						headers['Authorization'] = "Bearer {}".format(UPLOAD_API_TOKEN)
						response = requests.post("{}{}".format(API_BASE_URL, "media"), headers=headers, files=files)
					else:
						headers['Authorization'] = "Bearer {}".format(MEDIA_API_TOKEN)
						response = requests.post("{}{}".format(MEDIA_URL, "media"), headers=headers, files=files)
				except Exception as ex:
					pass
				else:
					if image_url in item['articles']:
						item_index = item['articles'].index(image_url)
						item['articles'][item_index] = """
							<img src="{}"><br>
						""".format(response.json()['source_url'])
					if image_url == item['thumbnail_url']:
						thumbnail_url = (response.json()['id'], response.json()['source_url'])
					image_ids.append((response.json()['id'], response.json()['source_url']))
				file.close()
				os.remove("{}/{}".format(IMAGES_STORE, image_path))
			headers = {'Authorization': "Bearer {}".format(UPLOAD_API_TOKEN)}
			categories = []
			try:
				response = requests.get("{}{}".format(API_BASE_URL, "categories"), headers=headers)
			except Exception as ex:
				pass
			else:
				for category in response.json():
					if category['name'] in CATEGORY_LIST:
						categories.append(category['id'])
			data = {
				'title': item['title'],
				'content': "<br> ".join(item['articles']),
				'status': "publish"
			}
			if categories:
				data['categories'] = categories
			if thumbnail_url:
				data['featured_media'] = thumbnail_url[0]
			try:
				response = requests.post("{}{}".format(API_BASE_URL, "posts"), headers=headers, data=data)
			except Exception as ex:
				pass
			else:
				print("{}	{}	{}".format("Success uploading to API.", item['response_url'], item['article_url']))

		return item