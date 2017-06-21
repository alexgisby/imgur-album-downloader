import os
from imgurdownloader import ImgurDownloader


all_imgur_url_possibilities = [
    "http://imgur.com/FVRUGe2",
    "http://imgur.com/FVRUGe2.jpg",
    "http://imgur.com/gallery/LHCvGPA",
    "http://imgur.com/r/awwnime/W7N6A",
    "http://i.imgur.com/j9W9tSi.jpg",
    "http://imgur.com/a/SVq41",
    "http://i.imgur.com/A61SaA1.gifv",
]


def test_single_img():
    imgur = ImgurDownloader('http://imgur.com/SnkkAVU')
    id = [('SnkkAVU', '.png')]
    assert(id == imgur.imageIDs)


def test_single_direct_link_img():
    imgur = ImgurDownloader('http://i.imgur.com/H37kxPH.jpg')
    id = [('H37kxPH', '.jpg')]
    assert(id == imgur.imageIDs)


def test_single_img_in_gallery():
    imgur = ImgurDownloader('http://imgur.com/gallery/40Uow1Q')
    id = [('40Uow1Q', '.jpg')]
    assert(id == imgur.imageIDs)


def test_single_img_in_album():
    imgur = ImgurDownloader('http://imgur.com/a/kfPrr')
    # NOTE: the single image and the album have different identifiers
    id = [('8sZQFxt', '.jpg')]
    assert(id == imgur.imageIDs)


def test_single_img_from_subreddit():
    imgur = ImgurDownloader('http://imgur.com/r/awwnime/YldNww8')
    id = [('YldNww8', '.png')]
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


def test_gifv_gif_direct_link():
    # since the extension is grabbed directly from the url, .gifv is the initial extension
    imgur = ImgurDownloader('http://i.imgur.com/MOvVbhc.gifv')
    ids = [('MOvVbhc', '.gifv')]
    assert (ids == imgur.imageIDs)

    # since the media is natively a video (.mp4) it is saved as such
    # NOTE: media downloaded is 1.4 MB
    imgur.save_images()
    file = os.path.join(os.getcwd(), 'MOvVbhc.mp4')
    assert(os.path.isfile(file))
    os.remove(file)


def test_gifv_gif_normal_link():
    imgur = ImgurDownloader('http://imgur.com/zvATqgs')
    ids = [('zvATqgs', '.gif')]
    assert(ids == imgur.imageIDs)
    imgur2 = ImgurDownloader('http://imgur.com/A61SaA1')
    ids2 = [('A61SaA1', '.gif')]
    assert(ids2 == imgur2.imageIDs)


if __name__ == "__main__":
    test_single_img()
