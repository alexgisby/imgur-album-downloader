import pytest

import sys
from os.path import dirname, abspath, join
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
