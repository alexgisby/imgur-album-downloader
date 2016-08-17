# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 09:40:27 2016

@author: j
"""

import imguralbum
import os

def main():
    url = 'http://imgur.com/gallery/3ypGJ' # anime recommendations
    url1 = 'http://imgur.com/a/SVq41' # bird comic
    url2 = 'http://imgur.com/SnkkAVU' # machines 4 colors
    url4 = 'http://imgur.com/gallery/40Uow1Q' # poopy butthole - single img 
    url5 = 'http://i.imgur.com/SnkkAVU.png' # machines 4 colors - direct link, single img
    
    dir1 = os.path.join(os.getcwd(), 'my-downloads')
#    print (dir1)
    downloader = imguralbum.ImgurAlbumDownloader(url5, dir1)
    downloader.save_images()
#    
if __name__ == '__main__':
    main()