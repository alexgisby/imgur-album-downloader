from setuptools import setup, find_packages

setup(
    name='Imgur Album Downloader',
    url='http://github.com/jmcurran/imgur-album-downloader/',
    author='Alex Gisby',
    author_email='alex@solution10.com',
    packages=find_packages(exclude=['tests*']),
    install_requires=['requests', 'pillow'],
    version='0.2-010',
    license='MIT',
    description='Download a whole Imgur album in one go',
    long_description=open('readme.md').read()
)