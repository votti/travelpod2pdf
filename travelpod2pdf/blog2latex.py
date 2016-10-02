# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 11:09:39 2014

@author: vitoz
"""

import pylatex as pytex
import travelpod2pdf.loadTravelpod as loadTP
import os
import glob
import pdb
from html import unescape


#clean up directories
#r = glob.glob(texPath+'*')
#for i in r:
#    os.remove(i)

 
class tp2latex(loadTP.TPloader):
    """ This class inherits from the TPloader class
        and will add the functionality to convert the
        loaded blog into a shiny latex file  """
    def __init__(self, filename, author, title, img_dir, packages=None,
                 img_widths=None, figure_position = '!htbp',
                 **kwargs):
        # initiate the latex document        
        """

        :rtype : object
        """
        self.doc = pytex.Document(default_filepath=filename, author=author,
                     title=title,**kwargs)

        if packages is not None:
            for pack in packages:
                self.doc.packages.append(pack)

        self.img_dir = img_dir

        if img_widths is None:
            self.img_widths = [r'150pt',r'250pt']
        else:
            self.img_widths = img_widths

        self.figure_position = figure_position
        self.censor_imgs = []
        
            
    def getMaintxt(self, sectionNr):
        # just very useful for debugging
        return(self.entryDict[sectionNr]['maintxt'])


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
        text = text.replace('#','\#')
        # replace superscripts
        return(text)
    
    
    def useImg(self, galleryImg):
        """ Only use images that contain a certain comment """
        if ('<p>  k </p>\n' in galleryImg['comments'].lower()) and not (
            os.path.basename(galleryImg['img']) in self.censor_imgs):
            return(True)
        else: 
            return(False)
    
    def getLatexImgs(self, entry, section):
        for img in entry['gallery']:
            if self.useImg(img):
                entry_dir = self.getImgFolder(entry, self.img_dir)
                if img['dims']['height'] > img['dims']['width']:
                    newpic = pytex.graphics.Figure(position=self.figure_position)
                    newpic.add_image(self.getImgPath(img,entry_dir),width=self.img_widths[0])

                else:
                    newpic = pytex.graphics.Figure(position=self.figure_position)
                    newpic.add_image(self.getImgPath(img,entry_dir),width=self.img_widths[1])

                if img['story'] != '':
                    newpic.add_caption(self.latexify(pytex.utils.bold(img['title']) + ': ' + img['story']))
                else:
                    newpic.add_caption(self.latexify(pytex.utils.bold(img['title'])))
                section.append(newpic)
    
    def createDoc(self):
        for entry in self.entryDict:
            section = pytex.Section(self.latexify(entry['title']))
            section.append(self.latexify(entry['maintxt']))
            self.getLatexImgs(entry,section)
            self.doc.append(section)
            
    def writeDoc(self, filepath=None, **kwargs):
        # self.doc.generate_tex()
        self.doc.generate_pdf(filepath=filepath, clean=False, **kwargs)
        # with open(texPath+'.tex', "w") as outfile:
        #    self.doc.dump(outfile)
  

# If called as a script
if __name__ == '__main__':

    url = 'http://www.travelpod.com/travel-blog/v_f/1/tpod.html'
    texPath = "/home/vitoz/Code/travelpod2pdf/data/"
    blogTitle = 'Reise um die halbe Welt'
    os.chdir(texPath)
    ## Test the class
    #url = 'http://www.travelpod.com/travel-blog/v_f/1/tpod.html'
    tp = tp2latex(filename='photibuech_letter',author='VF',title='Um die halbe Welt',
                  packages=[pytex.Package('morefloats'),
                             pytex.Package('geometry',options='letterpaper,margin=2cm,footskip=1cm')],
                  maketitle=True)

    imgDir ='/home/vitoz/Code/travelpod2pdf/data/img'
    

    tp.loadEntryDict('/home/vitoz/Code/travelpod2pdf/data/TPentries.json')
    tp.createDoc()
    tp.writeDoc()
    

     
#latexify(getMaintxt(5)).replace('\xe1\xb8\xa7','h')
#'ḧ'.encode('utf-8')
#text = 'ḧ'
#b'\xe1\xb8\xa7'.decode('utf-8')
#'ḧ'.encode('utf-8')
#'ā'.encode('utf-8')