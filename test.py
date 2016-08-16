# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 09:40:27 2016

@author: j
"""

import imguralbum

def main():
    url = 'http://imgur.com/gallery/3ypGJ' # anime recommendations
    url1 = 'http://imgur.com/a/SVq41' # bird comic
    url2 = 'http://imgur.com/SnkkAVU' # machines 4 colors
    url4 = 'http://imgur.com/gallery/40Uow1Q' # poopy butthole - single img 
    url5 = 'http://i.imgur.com/SnkkAVU.png' # machines 4 colors - direct link, single img
    
    downloader = imguralbum.ImgurAlbumDownloader(url5)
    downloader.save_images()
    
if __name__ == '__main__':
    main()