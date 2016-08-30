# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 09:40:27 2016

@author: j
"""

import imguralbum
import os

def test_dne():
    pass

def test():
    url1 = 'http://imgur.com/a/SVq41' # ALBUM, bird comic
    url3 = 'http://i.imgur.com/H37kxPH.jpg' # DIRECT IMAGE LINK, dog in vest - direct link, single img
    url2 = 'http://imgur.com/SnkkAVU' # SINGLE IMAGE, machines 4 colors
    url4 = 'http://imgur.com/gallery/40Uow1Q' # SINGLE IMAGE GALLERY, poopy butthole - single img 
    url5 = 'http://i.imgur.com/SnkkAVU.png' # DIRECT IMAGE LINK, machines 4 colors - direct link, single img
    url6 = 'http://imgur.com/a/kfPrr' # DNE SINGLE IMAGE ALBUM, man and dog
    url7 = 'http://i.imgur.com/A61SaA1.gifv' # .GIFV FILE, star wars
    
    
    dir1 = os.path.join(os.getcwd(), 'my-downloads')
#    print (dir1)
#    imguralbum.ImgurDownloader(url1, dir1, file_name='url1', debug=True).save_images()
#    print()
#    imguralbum.ImgurDownloader(url2, dir1, file_name='url2', debug=True).save_images()
#    print()
#    imguralbum.ImgurDownloader(url3, dir1, file_name='url3', debug=True).save_images()
#    print()
#    imguralbum.ImgurDownloader(url4, dir1, file_name='url4', debug=True).save_images()
#    print()
#    imguralbum.ImgurDownloader(url5, dir1, file_name='url5', debug=True).save_images()
#    print()
#    imguralbum.ImgurDownloader(url6, dir1, file_name='url6', debug=True).save_images()
    print()
    imguralbum.ImgurDownloader(url7, dir1, file_name='url7', debug=True).save_images()
    print()

    
if __name__ == '__main__':
    test()