# -*- coding: utf-8 -*-
import requests
import urllib
from bs4 import BeautifulSoup


# -------------------以下是数据操作
import sqlite3

# conn = sqlite3.connect('temp.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE record(id int(11) , title char(100))''')
# sql = 'INSERT INTO record VALUES( {}, {})'
# c.execute('''INSERT INTO record VALUES(1, '林依晨烫卷发显活力 着老气连衣裙似水桶')''')
# conn.commit()

def create_table():
    try:
        conn = sqlite3.connect('temp.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE record(id int(11) , title char(100))''')
        conn.commit()
    except:
        pass

def insert(id, title):
    conn = sqlite3.connect('temp.db')
    c = conn.cursor()
    try:
        sql = 'INSERT INTO record VALUES( {}, "{}")'.format(id, title)
        c.execute(sql)
        conn.commit()
        return True
    except:
        return False

def query(title):
    conn = sqlite3.connect('temp.db')
    c = conn.cursor()
    sql = 'select id from record where title = "{}" '.format(title)
    c.execute(sql)
    conn.commit()
    # print(c.fetchall(),type(c.fetchall()))

    if len(c.fetchall())>0:
        return True
    else:
        return False


# create_table()
# insert(1, "林依晨烫卷发显活力 着老气连衣裙似水桶")
# query( "林依晨烫卷发显活力 着老气连衣裙似水桶")
# query( "林依晨烫卷发显活力 着老气连衣裙似水桶sdfsdf")
# base_url = "http://www.duanzibar.com/wp-json/wp/v2/"
# -------------------以上是数据操作



base_url = "http://ylbgzx.com//wp-json/wp/v2/"
host_url = "http://ylbgzx.com"

def get_token():
    # token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9kdWFuemliYXIuY29tIiwiaWF0IjoxNDg1MzU0MDc4LCJuYmYiOjE0ODUzNTQwNzgsImV4cCI6MTQ4NTk1ODg3OCwiZGF0YSI6eyJ1c2VyIjp7ImlkIjoiMSJ9fX0.0qaQW1s6eTCXwVS-1rxvYG_KaXJ3WpGtL1iKpUga2Pw"
    # return token, token
    # url = "http://s1.imagescool.com/wp-json/jwt-auth/v1/token"
    url = "http://ylbgzx.com/wp-json/jwt-auth/v1/token"
    # data={"username":"mmkuser", "password":"$eQ1n9W@n9Zh@nM@nM@nK@n"}
    data={"username":"mmkuser", "password":"admin!2345"}
    res = requests.post(url, data=data)
    # print(res.status_code, res.text)
    if res.status_code == 200:
        return res,res.json()["token"]
# get_token()
def get_token_status(token):
    API = "/wp-json/jwt-auth/v1/token/validate"
    request_url = host_url+API
    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    res = requests.post(request_url, headers=headers)
    print(res.status_code, res.json())
    if res.status_code== 200:
        return token
    else:
        res, token = get_token()
        return token
# res, token = get_token()
# get_token_status(token)
# get_token_status("sui bian xie de yi ge zi fu chuan")

def post_img(image_path, token):
    # url = "http://s1.imagescool.com/wp-json/jwt-auth/v1/token"
    # data={"username":"mmkuser", "password":"$eQ1n9W@n9Zh@nM@nM@nK@n"}
    # res = requests.post(url, data=data)
    API_NAME = 'media'
    # base_url = 'http://s1.imagescool.com/wp-json/wp/v2/'
    url = base_url+API_NAME
    try:
        pic_data = urllib.request.urlopen(image_path).read()
    except:
        return None, None
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
    try:
        pic_data = urllib.request.urlopen(image_path).read()
    except:
        return {"status":"图片无法打开，返回原路径"}, '-1', image_path
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

def get_firstimg_url(html_scoure):
    bsp = BeautifulSoup(html_scoure, 'lxml')
    img_list = bsp.find_all('img')
    src_list = [i['src'] for i in img_list]
    try:
        return src_list[0]
    except:
        return None

def html_change_image_url(html_source):
    bsp = BeautifulSoup(html_source, 'lxml')
    img_list = bsp.find_all('img')
    src_list = [i['src'] for i in img_list]
    new_html_source = html_source
    for i in src_list:
        res, res_id, image_url = post_img_new(i)
        new_html_source = new_html_source.replace(i, image_url)
    del_ahref = bsp.find_all('a')
    for he in del_ahref:
        new_html_source = new_html_source.replace(he['href'],"")
    return new_html_source
html = '''<a href="1237861231y23ioy23oy12o3" title="nice">'''
print(html_change_image_url(html))

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
    # print(res.status_code, res, res.json())
    if res.status_code==500:
        return res,res.json()["data"]
    if res.status_code==201:
        return res, res.json()["id"]
    print('post_tags 运行错误  ',res.status_code, res.json(), '*'*100)
def post_article(title, content, tags, featured_media, token, cate,excerpt="" ):
    create_table()
    if query(title):
        print("已经抓取，跳过", -1, -1)
        return "已经抓取，跳过", -1, -1
    API_NAME = "posts"
    url = base_url + API_NAME
    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    data={"title":title, "content":content, "excerpt":excerpt, "tags":tags, "featured_media":featured_media, "status":"publish", "categories": cate}
    res = requests.post(url, headers=headers, data=data)
    if res.status_code == 201:
        insert(res.json()["id"],title)
    print(res, res.status_code, res.json()["id"])
    return res, res.status_code, res.json()["id"]

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
# tmp, status_code, id = post_article("这里是标题1", "这里是内容1", 1, token, 1)
# print(id,tmp,tmp)

# def parse_article(url):
#     res = requests.get(url)
#     bsp = BeautifulSoup(res.content, 'lxml')
#     # div[@class="article_content"]
#     cu_content = bsp.find("div",{"class":"article_content"})
#     center = cu_content.find("center")
#     print(center,'****'*20)
#     print(cu_content,'&&&&'*30)
#     return str(cu_content).replace(str(center),"")
#
# print(parse_article("http://www.huabian.com/mingxing/20170116/156612_2.html"))


