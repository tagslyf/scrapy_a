# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, os, requests, scrapy, uuid
from scrapy.pipelines.images import ImagesPipeline

from scrape_1024lualu_15.settings import API_BASE_URL, CATEGORY_LIST, IMAGES_STORE, MEDIA_URL, MEDIA_API_TOKEN, UPLOAD_API_TOKEN


class Scrape1024Lualu15Pipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):

	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):
		image_paths = [(x['path'], x['url']) for ok, x in results if ok]

		# for this site articles is only images. If no images downloaded it cannot be post.
		if image_paths:
			self.process_upload(item, image_paths)
		else:
			if item['image_urls']:
				for img_url in item['image_urls']:
					img_response = requests.get(img_url)
					if img_response.status_code in [200, 201]:
						filename = "full/{}.jpg".format(str(uuid.uuid4()).replace("-", ""))
						if not os.path.isdir("{}/full".format(IMAGES_STORE)):
							os.mkdir("{}/full".format(IMAGES_STORE))
						with open("{}/{}".format(IMAGES_STORE, filename), "wb") as f:
							for c in img_response:
								f.write(c)
						image_paths.append((filename, img_url))
						item['images'].append({'checksum': "", 'path': filename, 'url': img_url})
				self.process_upload(item, image_paths)
			else:
				print("{}	{}	{}	{}".format("Cannot upload to API.", item['response_url'][22:], item['article_url'][22:], item['title']))

		return item


	def process_upload(self, item, image_paths):
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
				if 'message' in response.json():
					for item_img in item['images']:
						if image_path == item_img['path']:
							tmp_index = item['images'].index(item_img)
							item_img['error'] = response.json()['message']
							item['images'][tmp_index] = item_img
					print("Error uploading media: 	{}	{}	{}".format(item['title'], filename, response.json()['message']))
				else:
					if image_url in item['articles']:
						item_index = item['articles'].index(image_url)
						item['articles'][item_index] = """
							<img src="{}"><br>
						""".format(response.json()['source_url'])
						if not item['thumbnail_url']:
							thumbnail_file = open("{}/{}".format(IMAGES_STORE, image_path), "rb")
							thumbnail_files = {
								'file': (filename, thumbnail_file, 'image/{}'.format(filename.split(".")[-1]))
							}
							thumbnail_headers = {'Authorization': "Bearer {}".format(UPLOAD_API_TOKEN)}
							thumbnail_response = requests.post("{}{}".format(API_BASE_URL, "media"), headers=thumbnail_headers, files=thumbnail_files)
							thumbnail_url = (thumbnail_response.json()['id'], thumbnail_response.json()['source_url'])
							item['thumbnail_url'] = thumbnail_response.json()['source_url']
							thumbnail_file.close()
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
			print("{}	{}	{}	{}".format("Success uploading to API.", item['response_url'][22:], item['article_url'][22:], item['title']))