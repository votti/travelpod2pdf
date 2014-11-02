# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 11:09:39 2014

@author: vitoz
"""

import pylatex as pytex
import loadTravelpod as loadTP
import os
import glob

url = 'http://www.travelpod.com/travel-blog/v_f/1/tpod.html'
texPath = "/home/vitoz/Git/travelpod2pdf/data/blog"
blogTitle = 'Reise um die halbe Welt'

#clean up directories
r = glob.glob(texPath+'*')
for i in r:
    os.remove(i)


lTP = loadTP.TPloader()
lTP.loadEntryDict('/home/vitoz/Git/travelpod2pdf/data/entries.json')

doc = pytex.Document(filename=texPath, author='WF',
                     title=blogTitle)

def getMaintxt(sectionNr):
    # just very usefull for debugging
    return(lTP.entryDict[sectionNr]['maintxt'])
    
def latexify(text):
    # here non latex conform symbols are replaced
    # replace strange newline character
    text = text.replace("\xa0", "\\newline \n")
    text = text.replace('\xb2','$^2$')
    text = text.replace('&','\&')
    text = text.replace(b'\xe1\xb8\xa7'.decode('utf-8'),'h')
    text = text.replace(b'\xc2\xb0'.decode('utf-8'),'$^\\circ$')
    text = text.replace(b'jo\xca\x8a\xcb\x88s\xc9\x9bm\xc9\x99ti'.decode('utf-8'),
    'Josemite')
    # replace superscripts
    return(text)


    
    
for entry in lTP.entryDict:
    section = pytex.Section(latexify(entry['title']))
    section.append(latexify(entry['maintxt']))
    doc.append(section)
  

with open(texPath+'.tex', "w") as outfile:
    doc.dump(outfile)
     
latexify(getMaintxt(5)).replace('\xe1\xb8\xa7','h')
'ḧ'.encode('utf-8')
text = 'ḧ'
b'\xe1\xb8\xa7'.decode('utf-8')
'ḧ'.encode('utf-8')
