# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .spiders.api_def import *

class BgxwPipeline(object):
    def process_item(self, item, spider):
        try:
            if len(item['content'])<1 or len(item['title'])<1:
                return None
        except:
            return None

        try:
            tmp, token = get_token()
        except:
            print('获取Token失败,无法继续')
            return None

        tmp, cate_id = post_category(spider.category, get_token_status(token))

        try:
            title = item['title'][0]
        except:
            return None

        # content = item['content'][0]
        try:
            content = html_change_image_url(item['content'][0])
        except:
            return None

        res, featured_media = post_img(get_firstimg_url(content), get_token_status(token))

        if featured_media == None:
            return None

        if 'http://www.huabian.com/uploadfile/' in content:
            return None

        try:
            tmp, tags = post_tags(item['tag'], get_token_status(token))
        except:
            tags = []
        tmp, status_code, id = post_article(title=title, content=content, tags=tags, featured_media=featured_media, token=get_token_status(token), cate=cate_id)



