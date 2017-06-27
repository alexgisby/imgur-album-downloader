from imgurdownloader.imgurdownloader import ImgurDownloader


def test_get_all_format_url():
    """convert add all path to imgur album."""
    url = 'https://imgur.com/a/p5wLR'
    exp_res = 'https://imgur.com/a/p5wLR/all'
    assert exp_res == ImgurDownloader.get_all_format_url(url)
