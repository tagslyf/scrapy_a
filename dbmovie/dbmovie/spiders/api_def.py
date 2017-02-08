# -*- coding: utf-8 -*-
import requests
import urllib

# base_url = "http://www.duanzibar.com/wp-json/wp/v2/"
base_url = "http://moviesky8.com/wp-json/wp/v2/"

def get_token():
    # token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9kdWFuemliYXIuY29tIiwiaWF0IjoxNDg1MzU0MDc4LCJuYmYiOjE0ODUzNTQwNzgsImV4cCI6MTQ4NTk1ODg3OCwiZGF0YSI6eyJ1c2VyIjp7ImlkIjoiMSJ9fX0.0qaQW1s6eTCXwVS-1rxvYG_KaXJ3WpGtL1iKpUga2Pw"
    # return token, token
    # url = "http://s1.imagescool.com/wp-json/jwt-auth/v1/token"
    url = "http://moviesky8.com/wp-json/jwt-auth/v1/token"
    # data={"username":"mmkuser", "password":"$eQ1n9W@n9Zh@nM@nM@nK@n"}
    data={"username":"mmkuser", "password":"admin!@#$%"}
    res = requests.post(url, data=data)
    # print(res.status_code, res.text)
    if res.status_code == 200:
        return res,res.json()["token"]
def post_img(image_path, token):
    # url = "http://s1.imagescool.com/wp-json/jwt-auth/v1/token"
    # data={"username":"mmkuser", "password":"$eQ1n9W@n9Zh@nM@nM@nK@n"}
    # res = requests.post(url, data=data)
    API_NAME = 'media'
    # base_url = 'http://s1.imagescool.com/wp-json/wp/v2/'
    url = base_url+API_NAME
    pic_data = urllib.request.urlopen(image_path).read()
    filename = image_path.split('/')[-1]

    files = {'file': (filename, pic_data, filename.split(".")[-1])}
    data = {"title":"filename", "status":"publish", "description":filename.split(".")[0]}
    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers['Content-Disposition'] = "attachment;filename={}".format(filename)
    res = requests.post(url, files=files, headers=headers, data=data)
    # print(res,res.text)
    if res.status_code == 201:
        return res, res.json()["id"]
def post_img_new(image_path):
    url = "http://s1.imagescool.com/wp-json/jwt-auth/v1/token"
    data={"username":"mmkuser", "password":"$eQ1n9W@n9Zh@nM@nM@nK@n"}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        tmp, token = response, response.json()["token"]
    # API_NAME = 'media'
    # base_url = 'http://s1.imagescool.com/wp-json/wp/v2/'
    # url_medit = base_url+API_NAME
    url_medit = 'http://s1.imagescool.com/wp-json/wp/v2/media'
    pic_data = urllib.request.urlopen(image_path).read()
    filename = image_path.split('/')[-1]

    files = {'file': (filename, pic_data, filename.split(".")[-1])}
    data = {"title":"filename", "status":"publish", "description":filename.split(".")[0]}
    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers['Content-Disposition'] = "attachment;filename={}".format(filename)
    res = requests.post(url_medit, files=files, headers=headers, data=data)
    # print(res,res.text)
    if res.status_code == 201:
        return res, res.json()["id"], res.json()["guid"]["rendered"]
def post_category(cate_name,token):
    API_NAME = 'categories'
    url = base_url + API_NAME
    data={"name":cate_name}
    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    res = requests.post(url, headers=headers, data=data)
    if res.status_code==500:
        return res,res.json()["data"]
    if res.status_code==201:
        return res, res.json()["id"]
    # return res, res.json()["name"]
    # print(res, res.status_code, res.json())
def post_tags(tag_name, token):
    API_NAME = 'tags'
    url = base_url + API_NAME
    data = {"name": tag_name}
    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    res = requests.post(url, headers=headers, data=data)
    print(res.status_code, res, res.json())
    if res.status_code==500:
        return res,res.json()["data"]
    if res.status_code==201:
        return res, res.json()["id"]
    print('post_tags 运行错误  ',res.status_code, res.json(), '*'*100)
def post_article(title, content, excerpt, featured_media, tags, token, cate):
    API_NAME = "posts"
    url = base_url + API_NAME
    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    data={"title":title, "content":content, "excerpt":excerpt, "featured_media":featured_media, "tags":tags, "status":"publish", "categories": cate}
    res = requests.post(url, headers=headers, data=data)
    return res, res.status_code

# token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9kdWFuemliYXIuY29tIiwiaWF0IjoxNDg2MTkxODQyLCJuYmYiOjE0ODYxOTE4NDIsImV4cCI6MTQ4Njc5NjY0MiwiZGF0YSI6eyJ1c2VyIjp7ImlkIjoiMSJ9fX0.8dpzfxWvVeajwBgnprSF3XoSjn88y1VwV5SdmsiKtWs"
# tmp, token = get_token()
# print(tmp, token)
# print(post_img("https://img1.doubanio.com/view/movie_poster_cover/spst/public/p2408407697.jpg",token))
# print(post_img("http://img.pconline.com.cn/images/upload/upc/tx/wallpaper/1308/15/c5/24496292_1376533594771.jpg",token))
# print(post_img_new("http://img.pconline.com.cn/images/upload/upc/tx/wallpaper/1308/15/c5/24496292_1376533594771.jpg"))
# print(post_category("标签3222",token))
# tmp, id = post_category("标签22",token)
# print(id,tmp)
# print(post_tags('%E6%83%8A%E6%A0%97',token))
# tmp, id = post_article("这里是标题1", "这里是内容1", "这里是简介1", 1, 4,5, token, 1)
# print(id,tmp,tmp.text)
