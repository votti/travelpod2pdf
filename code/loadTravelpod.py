# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 12:59:15 2014

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
    def getEntryDict(self,mainURL):
        req = self.loadURL(mainURL)
        tree = html.fromstring(req.text)
        #text_file = open("/home/vitoz/Documents/Output.txt", "w") 
        #text_file.write(req.content)
        #text_file.close()
        #http://www.w3schools.com/xpath/xpath_syntax.asp
        # get the html tags containing the link part to the entries and the 
        #titles
        tags = tree.xpath('//div[@class="blog_data"]/a[1]')
        # convert the html tags into proper lists
        entryDict = [dict(x.items()) for x in tags]
        # extract the entry id from href
        for entry in entryDict:
            entry['id'] = entry['href'].split('/')[4] 
        self.entryDict = entryDict
        
    def getEntryContents(self):
        for entry in self.entryDict:
            self.getEntryText(entry)
            self.getEntryGallery(entry)
    
    def saveEntryDict(self,fPath):
        with open(fPath, "w") as outfile:
            json.dump(self.entryDict, outfile, indent=4)
            
    def loadEntryDict(self,fPath):
        with open(fPath, "r") as impFile:
            self.entryDict = json.load(impFile)
    # Funktions to scrap data from the pages    
    def getEntryText(self,entry):
        entryURL =self.entryURL.replace('PASTEIDHERE',entry['id'])
        req = self.loadURL(entryURL)
        tree = html.fromstring(req.text)
        tags = tree.xpath('//div[@id="post"]/text()')
        entry['maintxt']="".join(tags).strip()       
        
    def getEntryGallery(self,entry):
        galleryURL =self.galleryURL.replace('PASTEIDHERE',entry['id'])
        req = self.loadURL(galleryURL)
        galDict=req.json()
        entry['gallery'] = galDict['data']
    
    def downloadImages(self,imgDir):
        # list all files in the directory
        curFiles=os.listdir(imgDir) 
        for entry in self.entryDict:
            pdb.set_trace()
            for photo in entry['gallery']: 
                #pdb.set_trace()
                imgURL = photo['img']
                #check if the image is already downloaded other
                imgName = imgURL.split('/')[-1]
                if imgName in curFiles:
                    continue
                urllib.urlretrieve(imgURL,os.path.join(imgDir,imgName))
                
    # Helper functions    
    def loadURL(self,url):
        req = requests.get(url)
        return(req)
        
if __name__ == '__main__':
    ## Test the class
    url = 'http://www.travelpod.com/travel-blog/v_f/1/tpod.html'
    loadTP = TPloader()
    loadTP.loadEntryDict('/home/vitoz/Git/travelpod2pdf/data/entries.json')
    #loadTP.getEntryDict(url)
    #loadTP.getEntryContents()
    #loadTP.saveEntryDict('/home/vitoz/Git/travelpod2pdf/data/entries.json')
    
    #loadTP.downloadImages('/home/vitoz/Git/travelpod2pdf/data/img')
    