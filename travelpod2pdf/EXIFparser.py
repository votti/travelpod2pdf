# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 14:05:55 2015

This class will allow get the exif data from files

It keeps to list
@author: vitoz
"""

import exifread
import os
import pdb

class EXIFparser(object):
    def __init__(self):
        self.files = set()
        self.exif_dict = dict()
        
    def add_files(self, newfiles):
        self.files.update(newfiles)
        
    def add_folder(self, folder, recursive=False,
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
        self.add_files(files)
        
        
    def read_exif(self, tags=None, details=False):
        if tags is None:
            tags = []
        self.exif_dict = {f: self._get_exif(f, tags, details)
            for f in self.files}
        
                                    
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
        print(img)
        return(exiftags)
        
if __name__ == '__main__':
    #import scipy as sp
    import matplotlib.pyplot as plt
    import collections
    ## Test the class
    targetDir ='/home/vitoz/Git/travelpod2pdf/data/img'
    targetImgs = EXIFparser()
    targetImgs.add_folder(targetDir,recursive=True)
    #targetImgs.read_exif(tags=['EXIF DateTimeOriginal','EXIF ShutterSpeedValue','EXIF ExposureTime'], details=False)
   
    # mounted with
    # with civfs2 installed
    # sudo mount.civfs https://url:port ~/mnt/home
    originalDir = '/home/vitoz/mnt/home/photo/VF Fotos/2014/Bilder Weltreise/'  
    originalImgs = EXIFparser()
    originalImgs.add_folder(originalDir,recursive=True)
    #originalImgs.files
    originalImgs.read_exif( details=True)
    
    # look at images with no tag
    #k = [k for k in imgM.original_dict.keys() if imgM.original_dict[k].__len__() != 1]
    #k = [k for k in imgM.original_dict.keys() if imgM.original_dict[k].__len__() is 1]
        
#    imgM._get_exif(k[0])
#    #img = sp.misc.imread(k[0])
#    img=plt.imread(k[0])
#    plt.imshow(img)
#    
#    dataTime = [imgM.target_dict[i]['EXIF DateTimeOriginal'].values for i in k]
#    
#    length = [imgM.original_dict[k].__len__() for k in imgM.original_dict.keys()]
#    [x for x, y in collections.Counter(length).items() if y > 1]
    # Return Exif tags
    #tags = exifread.process_file(f)
    # img server mount: sshfs -p ### ##@##:/mnt/synology/Bilder /home/vitoz/syn

    #loadTP.loadEntryDict('/home/vitoz/Git/travelpod2pdf/data/entries.json')

            
        
        

    
    
