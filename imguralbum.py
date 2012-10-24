#!/usr/bin/env python
# encoding: utf-8
"""
imguralbum.py - Download a whole imgur album in one go.

MIT License
Copyright Alex Gisby <alex@solution10.com>
"""

import sys
import re
import urllib
import os
import math

help_message = '''
Quickly and easily download an album from Imgur.

Format:
    $ python imguralbum.py [album URL] [destination folder]

Example:
    $ python imguralbum.py http://imgur.com/a/uOOju#6 /Users/alex/images

If you omit the dest folder name, the utility will create one with the same name as the
album (for example for http://imgur.com/a/uOOju it'll create uOOju/ in the cwd)

'''


class ImgurAlbumException(Exception):
    def __init__(self, msg=False):
        self.msg = msg


class ImgurAlbumDownloader:
    def __init__(self, album_url, output_messages=False):
        """
        Constructor. Pass in the album_url. Seeing as this is mostly a shell tool, you can have the
        class output messages too.
        """
        self.album_url = album_url
        self.output_messages = output_messages

        # Check the URL is actually imgur:
        match = re.match('http\:\/\/(www\.)?imgur\.com/a/([a-zA-Z0-9]+)(#[0-9]+)?', album_url)
        if not match:
            raise ImgurAlbumException("URL must be a valid Imgur Album")

        self.album_key = match.group(2)

        # Read the no-script version of the page for all the images:
        noscriptURL = 'http://imgur.com/a/' + match.group(2) + '/noscript'
        self.response = urllib.urlopen(noscriptURL)

        if self.response.getcode() != 200:
            raise ImgurAlbumException("Error reading Imgur: Error Code %d" % self.response.getcode())

    def save_images(self, foldername=False):
        """
        Saves the images from the album into a folder given by foldername.
        If no foldername is given, it'll use the album key from the URL.
        """
        html = self.response.read()
        self.images = re.findall('<img src="(http\:\/\/i\.imgur\.com\/([a-zA-Z0-9]+\.(jpg|jpeg|png|gif)))"', html)
        
        # Finding album name and setting it
        title = re.findall('<title>(.*)</title>', html, re.DOTALL)
        title = title[0]
        title = re.findall('(.*) - Imgur', title)
        title = title[0].strip()
        self.title = title

        if self.output_messages:
            print "Found %d images in album" % len(self.images)

        # Try and create the album folder:
        if foldername:
            albumFolder = foldername
        else:
            albumFolder = self.title

        if not os.path.exists(albumFolder):
            os.makedirs(albumFolder)
            print "Creating Album '%s'" % self.title

        # And finally loop through and save the images:
        for (counter, image) in enumerate(self.images, start=1):
            if self.output_messages:
                print "Fetching Image: " + image[0]
            prefix = "%0*d-" % (
                int(math.ceil(math.log(len(self.images) + 1, 10))),
                counter)
            path = os.path.join(albumFolder, prefix + image[1])
            urllib.urlretrieve(image[0], path)

        if self.output_messages:
            print ""
            print "Done!"


if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1:
        # Print out the help message and exit:
        print help_message
        exit()

    try:
        # Fire up the class:
        downloader = ImgurAlbumDownloader(args[1], output_messages=True)

        if len(args) == 3:
            albumFolder = args[2]
        else:
            albumFolder = False

        downloader.save_images(albumFolder)
        exit()
    except ImgurAlbumException as e:
        print "Error: " + e.msg
        print ""
        print help_message
        exit(1)
