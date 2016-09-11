#!/usr/bin/env python3
# encoding: utf-8


"""
imguralbum.py - Download a whole imgur album in one go.

Provides both a class and a command line utility in a single script
to download Imgur albums.

MIT License
Copyright Alex Gisby <alex@solution10.com>

Fork Created Aug. 2016 by jtara1
"""


import sys
import re
import urllib.request, urllib.parse, urllib.error
import os
import math
import time
from collections import Counter

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



class ImgurException(Exception):
    def __init__(self, msg=False):
        self.msg = msg


class ImgurDownloader:
    def __init__(self, album_url, dir_download=os.getcwd(), file_name='', delete_dne=True, debug=False):
        """
        Constructor. Pass in the album_url that you want to download.
        ARGUMENTS:
            album_url   : url of imgur gallery, album, single img, or direct url of image
            dir_download: core directory for location to save_images(...), (path passed in save_images(...) out prioritizes this one)
            file_name   : name of folder containing images from album or name of single image (depending on album_url)
                          if file_name given, it prioritizes over webpage title and imgur key
            debug       : if True, prints several variables throughout __init__(...)
        TODO:
            1. Regex used to get self.album_title (OS may not save acceptable characters in html in file names)
            3. Get individual image titles if provided (note: this is located in _item: {...}; section of html alongside image keys/hashes and extensions)
            4. Support downloading of an imgur user's entire album collection
        """
        (self.dir_root, tail) = os.path.split(__file__)

        self.album_url = album_url
        self.dir_download = dir_download # directory to save image(s)

        self.delete_dne = delete_dne
        self.debug = debug

        # Callback members:
        self.image_callbacks = []
        self.complete_callbacks = []

        # Check the URL is actually imgur:
        match = re.match("(https?)\:\/\/(www\.)?(i\.|m\.)?imgur\.com(/a|/gallery|/)/?([a-zA-Z0-9]+)(#[0-9]+)?(.\w*)?", album_url)
        if not match:
            raise ImgurException("URL must be a valid Imgur Album")

        self.protocol = match.group(1)
        self.direct_or_mobile = match.group(3) # could use a better var name
        self.imgur_link_type = match.group(4)
        if self.imgur_link_type == "/":
            self.is_album = False
        else:
            self.is_album = True
        self.album_key = match.group(5) # despite var name, this can refer to image key depending on album_url passed
        self.image_extension = match.group(7)

        if self.debug:
            print ("album key: " + self.album_key) # debug
            print ("is_album: " + str(self.is_album)) # debug

        if self.direct_or_mobile and self.image_extension:
            self.album_title = self.album_key if file_name == '' else file_name
            self.imageIDs = [(self.album_key, self.image_extension)]
            return

        if self.is_album:
            # Read the no-script version of the page for all the images:
            fullListURL = "http://imgur.com/a/" + self.album_key + "/layout/blog"
        elif not self.is_album:
            fullListURL = album_url

        try:
            self.response = urllib.request.urlopen(url=fullListURL)
            response_code = self.response.getcode()
        except Exception as e:
            self.response = False
            response_code = e.code

        if not self.response or self.response.getcode() != 200:
            raise ImgurException("Error reading Imgur: Error Code %d" % response_code)

        # Read in the images now so we can get stats and stuff:
        html = self.response.read().decode('utf-8')

        # default album_title
        self.album_title = self.album_key
        if file_name == '':
            # search for album / image title of webpage
            search = re.search("<title>\s*(.*) - (?:Album on )*?Imgur", html)
            if search:
                self.album_title = search.group(1) + ' (' + self.album_key + ')'
        elif file_name != '':
            self.album_title = file_name

        if self.debug:
            print ('album_title: ' + self.album_title) # debug

        # get section from html that contains image ID(s) and file extensions of each ID
        search = re.search('(_item:.*?};)', html, flags=re.DOTALL)
        if search:
            self.imageIDs = re.findall('.*?"hash":"([a-zA-Z0-9]+)".*?"ext":"(\.[a-zA-Z0-9]+)".*?', search.group(1))
            if len(self.imageIDs) > 1 and self.imageIDs[0][0] == self.album_key:
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


    def album_key(self):
        """
        Returns the key of this album. Helpful if you plan on generating your own
        folder names.
        """
        return self.album_key


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

        if not os.path.exists(dir_save):
            os.makedirs(dir_save)

        # And finally loop through and save the images:
        for (counter, image) in enumerate(self.imageIDs, start=1):
            key = image[0]
            ext = image[1]
            if ext == '.gifv':
                ext = '.webm'
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

            self.direct_download(image_url, path)

        # Run the complete callbacks:
        for fn in self.complete_callbacks:
            fn()

        self.dne_file.close()


    def direct_download(self, image_url, path):
        """ download data from url and save to path
            & optionally check if img downloaded is imgur dne file
        """
        if os.path.isfile(path):
            print ("Skipping, already exists.")
        else:
            try:
                # check if image is imgur dne image before we download anything
                if self.delete_dne:
                    req = urllib.request.urlopen(image_url)
                    if self.are_files_equal(req, self.dne_file):
                        if self.debug:
                            print ('[ImgurDownloader] DNE: %s' % path.split('/')[-1])
                        return

                # proceed with downloading if image is not dne or we're not checking for dne images
                urllib.request.urlretrieve(image_url, path)
            except Exception as e:
                print('[ImgurDownloader] %s' % e)
                os.remove(path)


    def urlretrieve_hook(self, trans_count, block_size, total_size):
        """ hook for urllib.request.urlretrieve(...) function, upon download complete, check if image dne """
        pass
        # if (trans_count * block_size) >= total_size:
        #     pass


    def is_imgur_dne_image(self, img_path):
        """ takes full image path & checks if bytes are equal to that of imgur does not exist image """
        dne_img = os.path.join(self.dir_root, 'imgur-dne.png') # edit location if needed
        with open(dne_img, 'rb') as f:
            dne_data = bytearray(f.read())
        with open(img_path, 'rb') as f:
            data = bytearray(f.read())
        # print('data_size %i data_dne_size %i' % (len(data), len(dne_data))) # the print that told me all
        if data == dne_data:
            return True
        else:
            return False


    def are_files_equal(self, file1, file2):
        """ given two file objects, checks to see if their bytes are equal """
        if bytearray(file1.read()) == bytearray(file2.read()):
            return True
        else:
            return False


    def remove_extension(self, path):
        """ Returns filename found in path by locating image file extension """

        exts = ['.png', '.jpg', 'webm', '.jpeg', '.jfif', '.gif', 'gifv', '.bmp', '.tif', '.tiff', '.webp', '.bpg', '.bat',
            '.heif', '.exif', '.ppm', '.cgm', '.svg']

        for e in exts:
            ext_index = path.find(e)
            if ext_index != -1:
                break
        if ext_index == -1: # no ext found in path
            return path
        return path[:ext_index]


if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1:
        # Print out the help message and exit:
        print (help_message)
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
        print (help_message)
        exit(1)
