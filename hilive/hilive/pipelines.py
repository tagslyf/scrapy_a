# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from hilive.settings import UPLOAD_API_TOKEN, IMAGES_STORE


class HilivePipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):

	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):
		# image_paths = [x['path'] for ok, x in results if ok]

		# api_base_url = "http://drzhan.com/wp-json/wp/v2/"
		# image_ids = []
		# content = ""
		# for image_path in image_paths:
		# 	headers = {}
		# 	headers['Authorization'] = "Bearer {}".format(UPLOAD_API_TOKEN)
		# 	headers['Content-Disposition'] = "attachment;filename={}".format(image_path.split("/")[-1])
		# 	file = open("{}/{}".format(IMAGES_STORE, image_path), "rb")
		# 	filename = image_path.split("/")[-1]
		# 	files = {
		# 		'file': (filename, file, 'image/{}'.format(filename.split(".")[-1]))
		# 	}
		# 	try:
		# 		response = requests.post("{}{}".format(api_base_url, "media"), headers=headers, files=files)
		# 	except Exception as ex:
		# 		pass
		# 	else:
		# 		content += """
		# 			<img src='{}'><br>
		# 		""".format(response.json()['source_url'])
		# 		image_ids.append((response.json()['id'], response.json()['source_url']))
		# 		file.close()
		# 		os.remove("{}/{}".format(IMAGES_STORE, image_path))

		# headers = {'Authorization': "Bearer {}".format(UPLOAD_API_TOKEN)}
		# data = {
		# 	'title': item['topic_title'],
		# 	'content': content,
		# 	'status': 'publish',
		# 	'featured_media': image_ids[0][0]
		# }
		# try:
		# 	response = requests.post("{}{}".format(api_base_url, "posts"), headers=headers, data=data)
		# except Exception as ex:
		# 	pass
		# else:
		# 	print("Success uploading to API.")

		# return item
		pass