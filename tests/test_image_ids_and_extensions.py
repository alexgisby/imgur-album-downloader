import pytest
from .imgurdownloader import ImgurDownloader

def test_single_img():
    imgur = ImgurDownloader('http://imgur.com/SnkkAVU')
    id = [('SnkkAVU', '.png')]
    assert(id == imgur.imageIDs)


def test_single_direct_link_img():
    imgur = ImgurDownloader('http://i.imgur.com/H37kxPH.jpg')
    id = [('H37kxPH', '.jpg')]
    assert(id == imgur.imageIDs)
    

def test_album_multi_img_with_gifv():
    imgur = ImgurDownloader('http://imgur.com/a/SVq41')
    ids = [('esSzNWQ', '.png'),
           ('z25tnfF', '.png'),
           ('eR27JxQ', '.png'),
           ('tsGMdgr', '.png'),
           ('cC0I2rs', '.png'),
           ('SzqTvSx', '.gif')]
    assert(ids == imgur.imageIDs)


if __name__ == "__main__":
    test_single_img()
