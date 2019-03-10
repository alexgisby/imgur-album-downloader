import pytest

import sys
from os.path import dirname, abspath, join
import os
__directory = dirname(abspath(__file__))
sys.path.append(join(__directory, '../' * 1))

from imgur_downloader.imgurdownloader import ImgurDownloader


@pytest.mark.parametrize(
    'url, exp_res',
    [
        (
            'https://imgur.com/a/p5wLR',
            'https://imgur.com/a/p5wLR/all'
        ),
        (
            'http://imgur.com/gallery/9niG9',
            'http://imgur.com/a/9niG9/all'
        ),
    ]
)
def test_get_all_format_url(url, exp_res):
    """convert add all path to imgur album."""
    assert exp_res == ImgurDownloader.get_all_format_url(url)


def test_redownload():
    url = 'https://imgur.com/gallery/4bv41a0'
    path = abspath(join(__file__, '..', 'my-downloads'))
    imgur = ImgurDownloader(url)

    file_names, skipped = imgur.save_images(path)
    assert(skipped == 0)

    _, skipped2 = imgur.direct_download(url, path)
    assert(skipped2 == 1)

    os.remove(join(path, file_names[0]))
