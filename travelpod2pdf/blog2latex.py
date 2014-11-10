# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 11:09:39 2014

@author: vitoz
"""

import pylatex as pytex
import loadTravelpod as loadTP
import os
import glob
import pdb
from html import unescape

url = 'http://www.travelpod.com/travel-blog/v_f/1/tpod.html'
texPath = "/home/vitoz/Git/travelpod2pdf/data/"
blogTitle = 'Reise um die halbe Welt'

os.chdir(texPath)
#clean up directories
#r = glob.glob(texPath+'*')
#for i in r:
#    os.remove(i)

 
class tp2latex(loadTP.TPloader):
    """ This class inherits from the TPloader class
        and will add the functionality to convert the
        loaded blog into a shiny latex file  """
    def __init__(self, filename, author, title, **kwargs):
        # initiate the latex document        
        self.doc = pytex.Document(filename=filename, author=author,
                     title=title,**kwargs)
        code = ''
        pytex.Varia('bla',package=['geometry'])
            
    def getMaintxt(self, sectionNr):
        # just very usefull for debugging
        return(lTP.entryDict[sectionNr]['maintxt'])

    
    def latexify(self, text):
        # here non latex conform symbols are replaced
        # replace strange newline character
        text = unescape(text)
        text = text.replace("\xa0", "\\newline \n")
        text = text.replace('\xb2', '$^2$')
        text = text.replace('&', '\&')
        text = text.replace(b'\xe1\xb8\xa7'.decode('utf-8'), 'h')
        text = text.replace(b'\xc2\xb0'.decode('utf-8'), '$^\\circ$')
        text = text.replace(b'jo\xca\x8a\xcb\x88s\xc9\x9bm\xc9\x99ti'.decode('utf-8'),
                        'Josemite')
        text = text.replace(b'\xc4\x81'.decode('utf-8'),'a')
        # replace superscripts
        return(text)
    
    
    def useImg(self, galleryImg):
        """ Only use images that (dont) contain a certain comment """
        if ('<p>  k </p>\n' in galleryImg['comments'].lower()):
            return(True)
        else: 
            return(False)
    
    def getLatexImgs(self, entry, section):
        for img in entry['gallery']:
            if self.useImg(img):
                newPic = pytex.pictures.Graphic(self.getImgPath(img,entry,imgDir),
                                                pos='!htbp',width='0.4')
                #pdb.set_trace()      
                if img['story'] != '':
                    newPic.add_caption(self.latexify(pytex.utils.bold(img['title']) + ': ' + img['story']))
                else:
                    newPic.add_caption(self.latexify(pytex.utils.bold(img['title'])))
                section.append(newPic)
    
    def createDoc(self):
        for entry in self.entryDict:
            section = pytex.Section(self.latexify(entry['title']))
            section.append(self.latexify(entry['maintxt']))
            self.getLatexImgs(entry,section)
            self.doc.append(section)
            
    def writeDoc(self):
        #self.doc.generate_tex()
        self.doc.generate_pdf(clean=False)        
        #with open(texPath+'.tex', "w") as outfile:
        #    self.doc.dump(outfile)
  

# If called as a script
if __name__ == '__main__':
    ## Test the class
    #url = 'http://www.travelpod.com/travel-blog/v_f/1/tpod.html'
    tp = tp2latex(filename='photibuech',author='VF',title='Um die halbe Welt')
    imgDir ='/home/vitoz/Git/travelpod2pdf/data/img'
    tp.loadEntryDict('/home/vitoz/Git/travelpod2pdf/data/entries.json')
    tp.createDoc()
    tp.writeDoc()
     
#latexify(getMaintxt(5)).replace('\xe1\xb8\xa7','h')
#'ḧ'.encode('utf-8')
#text = 'ḧ'
#b'\xe1\xb8\xa7'.decode('utf-8')
#'ḧ'.encode('utf-8')
#'ā'.encode('utf-8')