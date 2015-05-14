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
import pickle

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
        
    def save_exif_dict(self, fPath):
        with open(fPath, "wb") as outfile:
            pickle.dump(self.exif_dict, outfile)
            
            
    def load_exif_dict(self, fPath):
        with open(fPath, "rb") as impFile:
            self.exif_dict = pickle.load(impFile)
            
        
if __name__ == '__main__':
    #import scipy as sp
    import matplotlib.pyplot as plt
    import collections
    import numpy as np     ## Test the class
    
    doLoad = True
    originalDir = '/run/user/1000/gvfs/smb-share:server=synvotti,share=photo/VF Fotos/2014/Bilder Weltreise/'   
    targetDir = '/home/vitoz/Code/travelpod2pdf/data/img/'   
        
    # mounted with
    # with civfs2 installed
    # sudo mount.civfs https://url:port ~/mnt/home
    #originalDir = '/home/vitoz/mnt/home/photo/VF Fotos/2014/Bilder Weltreise/'  
    
 
    originalImgs = EXIFparser()
    
    if doLoad is True:
        originalImgs.load_exif_dict('/home/vitoz/Code/travelpod2pdf/data/originalImgsExif.pickle')
    else:   
        originalImgs.add_folder(originalDir,recursive=True)
        originalImgs.read_exif( details=False)
        originalImgs.save_exif_dict('/home/vitoz/Code/travelpod2pdf/data/originalImgsExif.pickle')
   
    #originalImgs.read_exif( details=True)
    #originalImgs.save_exif_dict('/home/vitoz/Code/travelpod2pdf/data/originalImgsExif_full.pickle')
    
    targetImgs = EXIFparser()
    
    if doLoad is True:
        targetImgs.load_exif_dict('/home/vitoz/Code/travelpod2pdf/data/targetImgsExif.pickle')
    else:
        targetImgs.add_folder(targetDir,recursive=True)
        targetImgs.read_exif( details=False)
        targetImgs.save_exif_dict('/home/vitoz/Code/travelpod2pdf/data/targetImgsExif.pickle')
        
        
        
    # Match the images by finding images with most matching fields
        
    
    nOrig = originalImgs.exif_dict.__len__()
    nTarget= targetImgs.exif_dict.__len__()
    keyList = next(iter(targetImgs.exif_dict.values())).keys()
    simMat = np.zeros((nTarget,nOrig),int)
    keyList = ['EXIF DateTimeOriginal']
        
    for (t, targetEntry) in enumerate(targetImgs.exif_dict.values()):
        for k in keyList:
            if k in targetEntry.keys():
                for (o, originalKey) in enumerate(originalImgs.exif_dict):
                    if k in originalImgs.exif_dict[originalKey].keys():
                        pdb.set_trace()
                        
                        simMat[t,o] =simMat[t,o] + int(targetEntry[k] == originalImgs.exif_dict[originalKey][k])
                        simMat[t,o] 
    
    oImg = '/run/user/1000/gvfs/smb-share:server=synvotti,share=photo/VF Fotos/2014/Bilder Weltreise/2014_03_05 Auckland/'
    tImg = '/home/vitoz/Code/travelpod2pdf/data/img/1394020787/1.1394020787.abflug.jpg'   


    oEntry = originalImgs.exif_dict[oImg]
    tEntry = targetImgs.exif_dict[tImg]
    # generate
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

            
        
        

    
    
