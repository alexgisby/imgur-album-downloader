import os

import pytest

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


@pytest.mark.parametrize(
    "url, exp_id", [
        ("http://imgur.com/SnkkAVU", [('SnkkAVU', '.png')]),
        ('http://i.imgur.com/H37kxPH.jpg', [('H37kxPH', '.jpg')]),
        ('http://imgur.com/gallery/jK0fB', [('vguHPLT', '.jpg')]),
        ('http://imgur.com/a/kfPrr', [('8sZQFxt', '.jpg')]),
        ('http://imgur.com/r/awwnime/YldNww8', [('YldNww8', '.png')]),
        (
            'http://imgur.com/a/SVq41',
            [
                ('esSzNWQ', '.png'),
                ('z25tnfF', '.png'),
                ('eR27JxQ', '.png'),
                ('tsGMdgr', '.png'),
                ('cC0I2rs', '.png'),
                ('SzqTvSx', '.gif')
            ]
        ),
        ('http://i.imgur.com/MOvVbhc.gifv', [('MOvVbhc', '.gifv')]),
        ('http://imgur.com/zvATqgs', [('zvATqgs', '.gif')]),
        ('http://imgur.com/A61SaA1', [('A61SaA1', '.gif')]),
    ],
)
def test_image_ids_and_extensions(url, exp_id):
    imgur = ImgurDownloader(url)
    assert(exp_id == imgur.json_imageIDs)
    assert(exp_id == imgur.imageIDs)


def test_gifv_gif_direct_link():
    # since the extension is grabbed directly from the url, .gifv is the initial extension
    imgur = ImgurDownloader('http://i.imgur.com/MOvVbhc.gifv')

    # since the media is natively a video (.mp4) it is saved as such
    # NOTE: media downloaded is 1.4 MB
    imgur.save_images()
    file = os.path.join(os.getcwd(), 'MOvVbhc.mp4')
    assert(os.path.isfile(file))
    os.remove(file)
