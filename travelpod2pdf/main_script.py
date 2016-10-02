__author__ = 'vitoz'


import os
import travelpod2pdf.loadTravelpod as loadTravelpod
import travelpod2pdf.blog2latex as blog2latex
import numpy as np
"""
This is the main script that does the conversion downloads a travelpod blog
"""

"""
Configuration
"""

# link to the blog
url = 'http://www.travelpod.com/travel-blog/v_f/1/tpod.html'
entryURL = "http://blog.travelpod.com/travel-blog-entries/v_f/1/PASTEIDHERE/tpod.html"
galleryURL = "http://www.travelpod.com/tools/pbrowser/v_f/1/PASTEIDHERE"


# link to a data directory to store cached data
data_dir = '/home/vitoz/Code/travelpod2pdf/data/'
# dir to store the tumbnail images
image_dir = '/home/vitoz/Code/travelpod2pdf/data/img'

# a list with image filenames to censor
with open('/home/vitoz/Code/travelpod2pdf/data/pictures_delete.csv','r') as dest_f:
    censor_imgs = [line.replace('\n','') for line in dest_f]

# Latex document
# blog title
latex_title = 'Reise um die halbe Welt'
latex_filename = 'photibuech_cesca_new'
latex_geometry = 'letterpaper,margin=2cm,footskip=1cm'
latex_author = 'v_f'

"""
Step 1: download the blog entries and thumbnail images from travelpod
"""

url = 'http://www.travelpod.com/travel-blog/v_f/1/tpod.html'

# intitialize already the blog2latex class
loadTP = blog2latex.tp2latex(filename=latex_filename, author=latex_author,title=latex_title, img_dir= image_dir,
              packages=[blog2latex.pytex.Package('morefloats'),
                        blog2latex.pytex.Package('geometry',options=latex_geometry)],
              maketitle=True)

loadTP.censor_imgs = censor_imgs

fn_entry_dict = os.path.join(data_dir,'TPentries.json')
if os.path.isfile(fn_entry_dict):
    loadTP.loadEntryDict(fn_entry_dict)
else:
    loadTP.getEntryDict(url, entryURL, galleryURL)
    loadTP.getEntryContents()
    loadTP.saveEntryDict('/home/vitoz/Code/travelpod2pdf/data/TPentries.json')

# download images if image dir is empty
if not os.listdir(image_dir):
    loadTP.downloadImages(image_dir)


"""
Step 2: save the blog as tex file
"""
os.chdir(data_dir)
loadTP.createDoc()
loadTP.writeDoc(filepath=data_dir)
