# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 14:05:55 2015

@author: vitoz
"""

import requests
from lxml import html
import urllib
import json
import pdb
import os

# pdb.set_trace()
# general info about scraping
# http://docs.python-guide.org/en/latest/scenarios/scrape/


class TPloader(object):
    def __init__(self):
        self.entryURL ='http://blog.travelpod.com/travel-blog-entries/v_f/1/PASTEIDHERE/tpod.html'
        self.galleryURL = 'http://www.travelpod.com/tools/pbrowser/v_f/1/PASTEIDHERE'
    
    
