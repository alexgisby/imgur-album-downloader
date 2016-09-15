#!/usr/bin/env python3
# encoding: utf-8


"""
imgurdownloader.py - Download a whole imgur album in one go.

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
import time
from collections import Counter

__doc__ = """
Quickly and easily download images from Imgur.

Format:
    $ python3 imgurdownloader.py [album URL] [destination folder]

Example:
    $ python3 imgurdownloader.py http://imgur.com/a/uOOju#6 /Users/alex/images

If you omit the dest folder name, the utility will create one with the same name
as the album
(for example for http://imgur.com/a/uOOju it'll create uOOju/ in the cwd)
"""



class ImgurException(Exception):
    def __init__(self, msg=False):
        self.msg = msg


class ImgurDownloader:
    def __init__(self, imgur_url, dir_download=os.getcwd(), file_name='',
                delete_dne=True, debug=False):
        """
        Constructor. Pass in the imgur_url that you want to download.
        Arguments:
            imgur_url: url of imgur gallery, album, single img, or direct url of image
            dir_download: core directory for location to save_images(...), (path passed in save_images(...) out prioritizes this one)
            file_name: name of folder containing images from album or name of single image (depending on imgur_url)
                          if file_name given, it prioritizes over webpage title and imgur key
            debug: if True, prints several variables throughout __init__(...)
        """
        (self.dir_root, tail) = os.path.split(__file__)

        self.imgur_url = imgur_url
        self.dir_download = dir_download # directory to save image(s)

        self.delete_dne = delete_dne
        self.debug = debug

        # Callback members:
        self.image_callbacks = []
        self.complete_callbacks = []

        # Check the URL is actually imgur:
        match = re.match(
            "(https?)\:\/\/(www\.)?(i\.|m\.)?imgur\.com/([a|gallery|r]?)/?([\w_]*)/?([\w_]*)(#[0-9]+)?(.\w*)?",
            imgur_url)
        if not match:
            raise ImgurException("URL must be a valid Imgur Album")

        self.protocol = match.group(1)
        domain_prefix = match.group(3)

        imgur_link_type = match.group(4)
        if imgur_link_type == '': # single imgur image
            self.is_album = False
        elif imgur_link_type == "r": # refers to subreddit categorized link
            self.is_album = False
            # reinitialize object with redirected URL
            # redirect_url = '%s://www.imgur.com/gallery/%s' % (match.group(1), match.group(6))
            # self.__init__(redirect_url, dir_download, file_name, delete_dne, debug)
        else:
            self.is_album = True

        # key is also referred to as hash in raw HTML
        self.main_key = match.group(5) if imgur_link_type != 'r' else match.group(6)
        image_extension = match.group(8)

        if self.debug:
            print ("main key: " + self.main_key) # debug

        # handle direct image links
        if domain_prefix and image_extension:
            self.album_title = self.main_key if file_name == '' else file_name
            self.imageIDs = [(self.main_key, image_extension)]
            return

        if self.is_album:
            # Read the no-script version of the page for all the images:
            fullListURL = "http://imgur.com/a/" + self.main_key + "/layout/blog"
        elif not self.is_album:
            fullListURL = imgur_url

        try:
            self.response = urllib.request.urlopen(url=fullListURL)
            response_code = self.response.getcode()
        except Exception as e:
            self.response = False
            response_code = e.code

        if not self.response or self.response.getcode() != 200:
            raise ImgurException("[ImgurDownloader] HTTP Response Code %d" % response_code)

        # Read in the images now so we can get stats and stuff:
        html = self.response.read().decode('utf-8')

        # default album_title
        self.album_title = self.main_key
        if file_name == '':
            # search for album / image title of webpage
            search = re.search("<title>\s*(.*) - (?:Album on )*?Imgur", html)
            if search:
                self.album_title = search.group(1) + ' (' + self.main_key + ')'
        elif file_name != '':
            self.album_title = file_name

        if self.debug:
            print ('album_title: ' + self.album_title) # debug

        # get section from html that contains image ID(s) and file extensions of each ID
        search = re.search('(_item:.*?};)', html, flags=re.DOTALL)
        if search:
            self.imageIDs = re.findall('.*?"hash":"([a-zA-Z0-9]+)".*?"ext":"(\.[a-zA-Z0-9]+)".*?', search.group(1))
            if len(self.imageIDs) > 1 and self.imageIDs[0][0] == self.main_key:
                self.imageIDs.remove(self.imageIDs[0]) # removes the first element in imageIDs since this'll could be the album_key if this link has more than 1 img

        if self.debug:
            print ("imageIDs count: " + str(len(self.imageIDs))) # debug
            print ("imageIDs:\n" + str(self.imageIDs)) # debug

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


    def get_album_key(self):
        """
        Returns the key of this album. Helpful if you plan on generating your own
        folder names.
        """
        return self.main_key


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


    def save_images(self, foldername=None):
        """
        Saves the images from the album into a folder given by foldername.
        If no foldername is given, it'll use the cwd and the album key.
        And if the folder doesn't exist, it'll try and create it.
        """
        # open imgur dne image to compare to downloaded image later
        dne_path = os.path.join(self.dir_root, 'imgur-dne.png')
        self.dne_file = open(dne_path, 'rb')

        # Try and create the album folder:
        albumFolder = ''
        if len(self.imageIDs) > 1:
            if foldername:
                albumFolder = foldername
            else:
                albumFolder = self.album_title

        dir_save = os.path.join(self.dir_download, albumFolder)

        downloaded = skipped = 0

        if not os.path.exists(dir_save):
            os.makedirs(dir_save)

        # return original content url & ext of .gifv link
        # gifv_regex = re.compile('<meta property="og:url" *content="([\w.:/?&]*?)"')
        # ext_regex = re.compile('.*?_item: .*?"ext":"(\.[a-zA-Z0-9]+)"', flags=re.DOTALL)
        def get_gifv_info(url, key, ext):
            """ Return original url & extension """
            if url.endswith('.gifv'):
                url = 'http://imgur.com/'+key
            req = urllib.request.urlopen(url)
            html = req.read().decode('utf-8')
            search = re.search(ext_regex, html)
            # either url wasn't a .gifv or regex search failed
            if not search:
                return url, ext
            orig_ext = search.group(1)
            return 'http://i.imgur.com/'+key+orig_ext, orig_ext

        # And finally loop through and save the images:
        for (counter, image) in enumerate(self.imageIDs, start=1):
            key = image[0]
            ext = image[1]
            # should be safe to save & open as .mp4
            if ext == '.gifv':
                ext = '.mp4'
                # image_url, ext = get_gifv_info(image_url, key, ext)
                # print('img_url: %s \next: %s' % (image_url, ext))

            image_url = "http://i.imgur.com/"+key+ext

            prefix = "%0*d-" % (
                int(math.ceil(math.log(len(self.imageIDs) + 1, 10))),
                counter
            )

            filename = prefix + key + ext
            if len(self.imageIDs) == 1:
                filename = self.album_title + ext
            path = os.path.join(dir_save, filename)

            # Run the callbacks:
            for fn in self.image_callbacks:
                fn(counter, image_url, path)

            dl, skp = self.direct_download(image_url, path)
            downloaded += dl
            skipped += skipped

        # Run the complete callbacks:
        for fn in self.complete_callbacks:
            fn()

        self.dne_file.close()
        return downloaded, skipped


    def direct_download(self, image_url, path):
        """ download data from url and save to path
            & optionally check if img downloaded is imgur dne file
        """
        def are_files_equal(file1, file2):
            """ given two file objects, checks to see if their bytes are equal """
            return True if bytearray(file1.read()) == bytearray(file2.read()) else False

        dl, skp = 0, 0
        if os.path.isfile(path):
            print ("[ImgurDownloader] Skipping, already exists.")
            skp = 1
        else:
            try:
                # check if image is imgur dne image before we download anything
                if self.delete_dne:
                    req = urllib.request.urlopen(image_url)
                    if are_files_equal(req, self.dne_file):
                        if self.debug:
                            print ('[ImgurDownloader] DNE: %s' % path.split('/')[-1])
                        return 0, 1

                # proceed with downloading if image is not dne or we're not checking for dne images
                urllib.request.urlretrieve(image_url, path)
                dl = 1
            except Exception as e:
                print('[ImgurDownloader] %s' % e)
                os.remove(path)
                skp = 1
        return dl, skp


    def is_imgur_dne_image(self, img_path):
        """ takes full image path & checks if bytes are equal to that of imgur does not exist image """
        dne_img = os.path.join(self.dir_root, 'imgur-dne.png') # edit location if needed
        with open(dne_img, 'rb') as f:
            dne_data = bytearray(f.read())
        with open(img_path, 'rb') as f:
            data = bytearray(f.read())
        return True if data == dne_data else False



if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1:
        # Print out the help message and exit:
        print (__doc__)
        exit()

    try:
        # Fire up the class:
        downloader = ImgurDownloader(args[1])

        print(("Found {0} images in album".format(downloader.num_images())))

        for i in downloader.list_extensions():
            print(("Found {0} files with {1} extension".format(i[1],i[0])))

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

    except ImgurException as e:
        print(("Error: " + e.msg))
        print ("")
        print ("How to use")
        print ("=============")
        print (__doc__)
        exit(1)
