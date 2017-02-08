# -*- coding: utf-8 -*-
import requests
import urllib
import re
from .spiders.api_def import get_token, post_img, post_img_new, post_category, post_tags, post_article
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



class DbmoviePipeline(object):
    def process_item(self, item, spider):
        if spider.name == "high_score_87movie" or spider.name == "tags_87movie":

            #获取token /wp-json/jwt-auth/v1/token
            try:
                tmp, token = get_token()
            except:
                print('获取Token失败,无法继续')
                return None


            #顶级目录
            tmp, cate_id = post_category(spider.category, token)

            #上传图片 /wp-json/wp/v2/media
            tmp, pic_id = post_img(item['pic'], token)
            tmp, pic, pic_url = post_img_new(item['pic'])
            pic_html = '<img src="{}" >'.format(pic_url)

            tmp, tags = post_tags(item['type'], token)

            #创建文章 /wp-json/wp/v2/posts
            download_html=""
            for i in item["download_url"]:
                download_html += i

            if len(item['content']) >0:
                content = item['content'][0]
            else:
                content = ""
            content = pic_html + content

            if len(item["synopsis"])>0:
                excerpt = item["synopsis"]
            else:
                excerpt = ""
            if len(item['name'])>0:
                title = item['name'][0]
            else:
                title = ""


            tmp, status_code = post_article(title=title,content=content+download_html,excerpt=excerpt,featured_media=pic_id,tags=tags,token=token, cate=cate_id)
            # print(status_code, '12345'*10)

        elif spider.name == "later_douban" or spider.name == "nowplay_dbmovie":
            # 获取token /wp-json/jwt-auth/v1/token
            try:
                tmp, token = get_token()
            except:
                print('获取Token失败,无法继续')
                return None

            # 顶级目录
            tmp, cate_id = post_category(spider.category, token)

            # 上传图片 /wp-json/wp/v2/media
            tmp, pic_id = post_img(item['pic'], token)
            tmp, pic, pic_url = post_img_new(item['pic'])
            pic_html = '<img src="{}" >'.format(pic_url)
            tags = []
            for i in item['type']:
                tmp, tag = post_tags(i, token)
                tags.append(tag)

            # 创建文章 /wp-json/wp/v2/posts
            if len(item['content']) > 0:
                content = item['content'][0]
            else:
                content = ""
            content = pic_html + content

            if len(item["synopsis"]) > 0:
                excerpt = item["synopsis"][0]
            else:
                excerpt = ""
            if len(item['name']) > 0:
                title = item['name'][0]
            else:
                title = ""


            tmp, status_code = post_article(title=title, content=content, excerpt=excerpt,featured_media=pic_id, tags=tags, token=token, cate=cate_id)
            # print(status_code, tmp, tmp.json(), '*标记*'*30)