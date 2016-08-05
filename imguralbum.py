#!/usr/bin/env python3
# encoding: utf-8


"""
imguralbum.py - Download a whole imgur album in one go.

Provides both a class and a command line utility in a single script
to download Imgur albums.

MIT License
Copyright Alex Gisby <alex@solution10.com>
"""


import sys
import re
import urllib.request, urllib.parse, urllib.error
import os
import math
from collections import Counter
from traceback import format_exc
import platform


help_message = """
Quickly and easily download an album from Imgur.

Format:
    $ python imguralbum.py [album URL] [destination folder]

Example:
    $ python imguralbum.py http://imgur.com/a/uOOju#6 /Users/alex/images

If you omit the dest folder name, the utility will create one with the same name
as the album
(for example for http://imgur.com/a/uOOju it'll create uOOju/ in the cwd)
"""


class ImgurAlbumException(Exception):
    def __init__(self, msg=False):
        self.msg = msg


class ImgurAlbumDownloader:
    def __init__(self, album_url):
        """
        Constructor. Pass in the album_url that you want to download.
        """
        self.album_url = album_url

        # Callback members:
        self.image_callbacks = []
        self.complete_callbacks = []

        # Check the URL is actually imgur:
        match = re.match("(https?)\:\/\/(www\.)?(?:m\.)?imgur\.com\/(a|gallery|topic)\/([a-zA-Z0-9]+)\/?(#[0-9]+|[a-zA-Z0-9]+)?", album_url)
        if not match:
            raise ImgurAlbumException("URL must be a valid Imgur Album")

        if match.group(3) == "topic":
            self.album_key = match.group(5)
        else:
            self.album_key = match.group(4)

        # Read full page album, gallery or topic to get all the images:
        fullListURL = "http://imgur.com/a/" + self.album_key + "/layout/blog"

        try:
            self.response = urllib.request.urlopen(url=fullListURL)
            response_code = self.response.getcode()
        except Exception as e:
            self.response = False
            response_code = e.code

        if not self.response or self.response.getcode() != 200:
            raise ImgurAlbumException("Error reading Imgur: Error Code %d" % response_code)

        # Read in the images now so we can get stats and stuff:
        html = self.response.read().decode('utf-8')

        self.album_title = re.search('images?\s*:\s*{"id":"%s".*?"title":"(.*?)"' % self.album_key.strip() ,html).group(1)

        html = html.splitlines()
        for line in html:
            line=line.lstrip()
            if line.startswith('_item:') or line.startswith('images'):
                self.imageIDs = re.findall('.*?{"hash":"([a-zA-Z0-9]+)".*?"ext":"(\.[a-zA-Z0-9]+)".*?', line)
                break

        self.cnt = Counter()
        for i in self.imageIDs:
            self.cnt[i[1]] += 1


    def num_images(self):
        """
        Returns the number of images that are present in this album.
        """
        return len(self.imageIDs)


    def list_extensions(self):
        """
        Returns list with occurrences of extensions in descending order.
        """
        return self.cnt.most_common()


    def album_key(self):
        """
        Returns the key of this album. Helpful if you plan on generating your own
        folder names.
        """
        return self.album_key

    def album_title(self):
        """
        Returns the title of this album.
        """
        return self.album_title

    def on_image_download(self, callback):
        """
        Allows you to bind a function that will be called just before an image is
        about to be downloaded. You'll be given the 1-indexed position of the image, it's URL
        and it's destination file in the callback like so:
            my_awesome_callback(1, "http://i.imgur.com/fGWX0.jpg", "~/Downloads/1-fGWX0.jpg")
        """
        self.image_callbacks.append(callback)


    def on_complete(self, callback):
        """
        Allows you to bind onto the end of the process, displaying any lovely messages
        to your users, or carrying on with the rest of the program. Whichever.
        """
        self.complete_callbacks.append(callback)


    def save_images(self, foldername=False):
        """
        Saves the images from the album into a folder given by foldername.
        If no foldername is given, it'll use the cwd and the album key.
        And if the folder doesn't exist, it'll try and create it.
        """
        # Try and create the album folder:
        if foldername:
            albumFolder = foldername
        elif self.album_title is None or self.album_title is "":
            print("Album has no name, it will be named after ID contained in album URL.\n")
            albumFolder = self.album_title = self.album_key
        else:
            if platform.system() == "Windows":
               albumFolder= self.album_title.translate({ord(i):' ' for i in "/\*?<>|"})
            else:
                albumFolder = self.album_title.translate({ord(i):' ' for i in "/"})

        if not os.path.exists(albumFolder):
            os.makedirs(albumFolder)

        # And finally loop through and save the images:
        for (counter, image) in enumerate(self.imageIDs, start=1):
            image_url = "http://i.imgur.com/"+image[0]+image[1]

            prefix = "%0*d-" % (
                int(math.ceil(math.log(len(self.imageIDs) + 1, 10))),
                counter
            )
            path = os.path.join(albumFolder, prefix + image[0] + image[1])

            # Run the callbacks:
            for fn in self.image_callbacks:
                fn(counter, image_url, path)

            # Actually download the thing
            if os.path.isfile(path):
                print ("Skipping, already exists.\n")
            else:
                try:
                    urllib.request.urlretrieve(image_url, path)
                except:
                    print ("Download failed.\n"+format_exc())
                    os.remove(path)

        # Run the complete callbacks:
        for fn in self.complete_callbacks:
            fn()


if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1:
        # Print out the help message and exit:
        print (help_message)
        exit()

    try:
        # Fire up the class:
        downloader = ImgurAlbumDownloader(args[1])

        print(("\nFound {0} images in album called \"{1}\"\n".format(downloader.num_images(),downloader.album_title)))

        for i in downloader.list_extensions():
            print(("Found {0} files with {1} extension".format(i[1],i[0])))
        print()

        # Called when an image is about to download:
        def print_image_progress(index, url, dest):
            print(("Downloading Image %d" % index))
            print(("    %s >> %s" % (url, dest)))
        downloader.on_image_download(print_image_progress)

        # Called when the downloads are all done.
        def all_done():
            print ("")
            print ("Done!")
        downloader.on_complete(all_done)

        # Work out if we have a foldername or not:
        if len(args) == 3:
            albumFolder = args[2]
        else:
            albumFolder = False

        # Enough talk, let's save!
        downloader.save_images(albumFolder)
        exit()
        
    except ImgurAlbumException as e:
        print(("Error: " + e.msg))
        print ("")
        print ("How to use")
        print ("=============")
        print (help_message)
        exit(1)
