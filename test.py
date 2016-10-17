# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 09:40:27 2016

@author: j
"""

import imgurdownloader as imguralbum
import os
import time


def test():
    url1 = 'http://imgur.com/a/SVq41' # ALBUM, bird comic
    url2 = 'http://imgur.com/SnkkAVU' # SINGLE IMAGE, machines 4 colors
    url3 = 'http://i.imgur.com/H37kxPH.jpg' # DIRECT IMAGE LINK, dog in vest - direct link, single img
    url4 = 'http://imgur.com/gallery/40Uow1Q' # SINGLE IMAGE GALLERY, poopy butthole - single img
    url5 = 'http://i.imgur.com/SnkkAVU.png' # DIRECT IMAGE LINK, machines 4 colors - direct link, single img
    url6 = 'http://imgur.com/a/kfPrr' # DNE SINGLE IMAGE ALBUM, man and dog
    url7 = 'http://i.imgur.com/A61SaA1.gifv' # .GIFV FILE, star wars
    url_dne = 'http://i.imgur.com/removed.png' # DIRECT IMAGE LINK, imgur link to dne image
    url8 = 'http://imgur.com/a/uOOju#6' # ALBUM, bikes
    url9 = 'http://imgur.com/r/awwnime/YldNww8' # /r/Awwnime LINK, snake girl
    url10 = 'http://imgur.com/r/awwnime/W7N6A' # /r/Awwnime ALBUM LINK, anime girl HTTP ERROR 404
    url11 = 'http://imgur.com/r/awwnime/poDoh' # /r/Awwnime ALBUM LINK, anime girl w/ bow


    dir1 = os.path.join(os.getcwd(), 'my-downloads')
    rand_name = str(int(time.time()))
    print (dir1)
    print(imguralbum.ImgurDownloader(url1, dir1, file_name=rand_name, debug=True).save_images())
    print()
    imguralbum.ImgurDownloader(url2, dir1, file_name='url2', debug=True).save_images()
    print()
    imguralbum.ImgurDownloader(url3, dir1, file_name='url3', debug=True).save_images()
    print()
    # imguralbum.ImgurDownloader(url4, dir1, file_name='url4', debug=True).save_images()
    print()
    # imguralbum.ImgurDownloader(url5, dir1, file_name='url5', debug=True).save_images()
    # print()
    # imguralbum.ImgurDownloader(url6, dir1, file_name='url6', debug=True).save_images()
    print()
    # print(imguralbum.ImgurDownloader(url7, dir1, file_name=rand_name, delete_dne=False, debug=True).save_images())
    print()
    print(imguralbum.ImgurDownloader(url_dne, dir1, file_name=rand_name, debug=True).save_images())
    # print()
    # imguralbum.ImgurDownloader(url8, dir1, file_name='url8', debug=True).save_images()
    # print()
    # imguralbum.ImgurDownloader(url9, dir1, file_name='url9', debug=True).save_images()
    # print()
    # imguralbum.ImgurDownloader(url10, dir1, file_name='url10', debug=True).save_images()
    # print()
    # imguralbum.ImgurDownloader(url11, dir1, file_name='url11', debug=True).save_images()
    #

def test_dne(path):
    dne_file = open(os.path.join(os.getcwd(), 'imgur-dne.png'), 'rb')

    def are_files_equal(file1, file2):
        """ given two file objects, checks to see if their bytes are equal """
        if bytearray(file1.read()) == bytearray(file2.read()):
            return True
        else:
            return False

    def remove_extension(path):
        """ Returns filename found in path by locating image file extension """
        exts = ['.png', '.jpg', '.mp4', 'webm', '.jpeg', '.jfif', '.gif', 'gifv',
                '.bmp', '.tif', '.tiff', '.webp', '.bpg', '.bat',
                '.heif', '.exif', '.ppm', '.cgm', '.svg']
        for e in exts:
            ext_index = path.find(e)
            if ext_index != -1:
                break
        if ext_index == -1: # no ext found in path
            return path
        return path[:ext_index]

    filename = remove_extension(path)
    with open(path, 'rb') as file:
        if are_files_equal(file, dne_file):
            print ('DNE: ', filename)
            print ('Deleting DNE image.')
            # os.remove(path)
        else:
            print('not dne img')

if __name__ == '__main__':
    test()
    # path_dne = os.path.join(os.getcwd(), 'imgur-dne.png')
    # path_img = os.path.join(os.getcwd(), 'test-img.png')
    # test_dne(path_img)
    pass
