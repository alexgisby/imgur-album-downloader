from setuptools import setup

setup(
    name = 'Imgur Album Downloader',
    url = 'http://github.com/jmcurran/imgur-album-downloader/',
    author = 'Alex Gisby',
    author_email = 'alex@solution10.com',
    packages = ['ImgurAlbumDownloader'],
    install_requires = ['requests', 'pillow'],
    version = '0.1',
    license = 'MIT',
    description = 'Download a whole Imgur album in one go',
    long_description = open('readme.md')
)