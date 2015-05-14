# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 14:05:55 2015

This class will allow to match files based on the exif id.

It keeps to lists of paths of target and orignial files with the attributes
.target_files and original_files
@author: vitoz
"""

import exifread
import os
import pdb
import pickle

class ImageMatcher(object):
    def __init__(self):
        self.target_files = set()
        self.original_files = set()
        self.target_dict = dict()
        self.original_dict = dict()
    def add_target_files(self, files):
        self._add_files(files, self.target_files)
        
    def add_original_files(self, files):
        self._add_files(files, self.original_files)
        
    def add_target_folder(self, folder, recursive=False,
                          ext = None):
        if ext is None:
            ext = ['.jpg','.jpeg']
        self._add_folder(folder, self.target_files, recursive, ext)
        
    def add_original_folder(self, folder, recursive=False,
                          ext = None):
        if ext is None:
            ext = ['.jpg','.jpeg']
        self._add_folder(folder, self.original_files, recursive, ext)
        
    @classmethod                        
    def _add_files(self, files, tlist):
        tlist.update(files)
    
    @classmethod    
    def _add_folder(self, folder, tlist, recursive=False,
                          ext=None):
        if ext is None:
            ext = ['.jpg','.jpeg']
            
        if isinstance(ext,list):
            ext = tuple(ext)              
            
        folder = os.path.expanduser(folder)
        # For the recursive case:
        if recursive:
            files = [os.path.join(dp, f) for dp, dn, fn in 
                os.walk(folder) for f in fn]
        else:
            files = [os.path.join(folder, f) for f in os.listdir(folder)]
            
        files = [f for f in files if f.lower().endswith(ext)]
        self._add_files(files,tlist)
        
        
    def read_exif(self, tags=None, details=False):
        if tags is None:
            tags = []
        files = self.original_files
        self.original_dict = {f: self._get_exif(f, tags, details)
            for f in files}
        
        files = self.target_files
        self.target_dict =  {f: self._get_exif(f, tags, details)
                                for f in files}
                                    
    @classmethod                                    
    def _get_exif(self, img, tags=None, details=False):
        if tags is None:
            tags = []
        # Reads the exif
        f = open(img, 'rb')
        
        if tags.__len__() == 0:
            exiftags = exifread.process_file(f, details=details)
                    
        elif tags.__len__() == 1:
            exiftags = exifread.process_file(f, details=details, stop_tag=tags[0])
            #pdb.set_trace()            
            exiftags = {t: exiftags[t] for t in tags if t in exiftags.keys()}
            
        else:
            exiftags = exifread.process_file(f, details=details)
            exiftags = {t: exiftags[t] for t in tags if t in exiftags.keys()}
            
        return(exiftags)
        
if __name__ == '__main__':
    #import scipy as sp
    import matplotlib.pyplot as plt
    import collections
    ## Test the class
    imgDir ='/home/vitoz/Git/travelpod2pdf/data/img'
    imgM = ImageMatcher()
    imgM.add_target_folder(imgDir,recursive=True)
    imgM.add_original_folder(imgDir,recursive=True)
    
    imgM.read_exif(tags=['EXIF DateTimeOriginal','EXIF ShutterSpeedValue','EXIF ExposureTime'], details=False)
    
    # look at images with no tag
    #k = [k for k in imgM.original_dict.keys() if imgM.original_dict[k].__len__() != 1]
    #k = [k for k in imgM.original_dict.keys() if imgM.original_dict[k].__len__() is 1]
        
    imgM._get_exif(k[0])
    #img = sp.misc.imread(k[0])
    img=plt.imread(k[0])
    plt.imshow(img)
    
    dataTime = [imgM.target_dict[i]['EXIF DateTimeOriginal'].values for i in k]
    
    length = [imgM.original_dict[k].__len__() for k in imgM.original_dict.keys()]
    [x for x, y in collections.Counter(length).items() if y > 1]
    # Return Exif tags
    #tags = exifread.process_file(f)
    # img server mount: sshfs -p ### ##@##:/mnt/synology/Bilder /home/vitoz/syn

    #loadTP.loadEntryDict('/home/vitoz/Git/travelpod2pdf/data/entries.json')

            
        
        

    
    
