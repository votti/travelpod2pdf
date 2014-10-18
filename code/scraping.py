# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/vitoz/.spyder2/.temp.py
"""

from lxml import html
import requests

def tree_from_website(site):
    page = requests.get(site)
    tree = html.fromstring(page.text)
    return(tree)

site='http://blog.travelpod.com/travel-blog-entries/v_f/1/1401131153/tpod.html'
tree = tree_from_website(site)

links = tree.xpath('//div[@id="post"]/text()')

# get maintext
main =  tree.xpath('//div[@id="post"]/text()')

# get the links to the photos

linkphot =tree.xpath('//meta[@property="og:image"]/@content')


tree2=tree_from_website('http://blog.travelpod.com/travel-blog-entries/v_f/1/1401131153/tpod.html#pbrowser/v_f/1/1401131153/filename=yoga-mit-fl-te.jpg')
story =  tree2.xpath('//div[@class="story"]/@style')


## other approach
import codecs
import lxml.html as lh
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://blog.travelpod.com/travel-blog-entries/v_f/1/1401131153/tpod.html#pbrowser/v_f/1/1401131153/filename=yoga-mit-fl-te.jpg')
content = browser.page_source
browser.quit()
tree3=html.fromstring(content)
tree3.xpath('//div[@class="story"]/@style')

import requests

req = requests.get(url='http://blog.travelpod.com/travel-blog-entries/v_f/1/1401131153/tpod.html#pbrowser/v_f/1/1401131153/filename=yoga-mit-fl-te.jpg',
       headers = {"Referer": "http://blog.travelpod.com/travel-blog-entries/v_f/1/1401131153/tpod.html",
          "X-Requested-With": "XMLHttpRequest"})
lines = ''          


text_file = open("/home/vitoz/Documents/Output.txt", "w") 
for line in  req.iter_lines():
    text_file.write(line +'\n')
text_file.close()

# This is the real link for the pictures 
url = 'http://www.travelpod.com/tools/pbrowser/v_f/1/1401131153'

import requests
r = requests.get(url)
data = r.json()

# we can compare/find photos via the File Number id from the webphotos




import scrapy

req = scrapy.http.Request(url='http://blog.travelpod.com/travel-blog-entries/v_f/1/1401131153/tpod.html#pbrowser/v_f/1/1401131153/filename=yoga-mit-fl-te.jpg',
       headers = {"Referer": "http://blog.travelpod.com/travel-blog-entries/v_f/1/1401131153/tpod.html",
          "X-Requested-With": "XMLHttpRequest"})
          
parser =scrapy.spider.BaseSpider


