#!/usr/bin/env python3
# encoding: utf-8


"""
imgur_downloader.py - Download a whole imgur album in one go.

Provides both a class and a command line utility in a single script
to download Imgur albums.

MIT License
Copyright Alex Gisby <alex@solution10.com>
"""

from collections import Counter
from urllib.error import HTTPError
from urllib.parse import urlparse
import json
import logging
import math
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import unicodedata
import click


__doc__ = """
Quickly and easily download images from Imgur.

Format:
    $ imgur_downloader [album URL] [destination folder]

Example:
    $ imgur_downloader http://imgur.com/a/uOOju#6 /Users/alex/images

If you omit the dest folder name, the utility will create one with the same name
as the album
(for example for http://imgur.com/a/uOOju it'll create uOOju/ in the cwd)
"""


class ImgurException(Exception):
    """General exception class for errors from Imgur & this program"""
    def __init__(self, msg=False):
        self.msg = msg


class FileExistsException(ImgurException):
    """Exception for when file already exists locally"""


class ImgurDownloader:
    """Parses imgur and downloads image(s)"""

    def __init__(self, imgur_url, dir_download=os.getcwd(), file_name='',
                 delete_dne=True, debug=False):
        """Gather imgur hashes & extensions from the url passed

        :param imgur_url: url of imgur gallery, album, single img, or direct
            url of image
        :param dir_download: core directory to save_images(...),
            (directory passed in save_images(...) out prioritizes this one)
        :param file_name: name of folder containing images from album or name
            of single image (depending on imgur_url) if file_name given,
            it prioritizes over webpage title and imgur key
        :param delete_dne: prevent downloading of Imgur Does Not Exist image
            if encountered
        :param debug: prints several variables throughout the class

        :rtype: None
        """
        self.dir_root = os.path.dirname(os.path.abspath(__file__))
        self.dne_path = os.path.join(self.dir_root, 'imgur-dne.png')

        self.imgur_url = imgur_url
        # directory to save image(s)
        self.dir_download = os.path.abspath(dir_download)

        self.delete_dne = delete_dne
        self.debug = debug

        self.log = logging.getLogger('ImgurDownloader')

        # Callback members:
        self.image_callbacks = []
        self.complete_callbacks = []

        # Check the URL is actually imgur:
        match = re.match(
            "(https?)://(www\.)?(i\.|m\.)?imgur\.com/(a/|gallery/|r/)?/?(\w*)/?(\w*)(#[0-9]+)?(.\w*)?",  # NOQA
            imgur_url)
        if not match:
            raise ImgurException("URL must be a valid Imgur Album")

        self.protocol = match.group(1)
        # domain_prefix = match.group(3)

        imgur_link_type = match.group(4)

        # key is also referred to as hash in raw HTML
        self.main_key = match.group(5) \
            if imgur_link_type != 'r' else match.group(6)
        image_extension = match.group(8)

        if self.debug:
            print("imgur_link_type: {}".format(imgur_link_type))
            print("main key: " + self.main_key)  # debug

        # handle direct image links
        if image_extension:
            self.album_title = self.main_key if file_name == '' \
                else slugify(file_name)
            self.imageIDs = [(self.main_key, image_extension)]
            # copy imageIDs to json_imageIDs for direct image link
            self.json_imageIDs = self.imageIDs
            return

        imgur_url = self.get_all_format_url(imgur_url)
        # e.g.: imgur.com/a/p5wLR -> imgur.com/a/p5wLR/all
        try:
            self.response = urllib.request.urlopen(url=imgur_url)
            response_code = self.response.getcode()
        except Exception as e:
            self.response = False
            try:
                response_code = e.code
            except AttributeError:
                raise e

        if not self.response or self.response.getcode() != 200:
            raise ImgurException("[ImgurDownloader] HTTP Response Code %d"
                                 % response_code)

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

        # remove invalid filename characters
        self.album_title = slugify(self.album_title)

        if self.debug:
            print('album_title: ' + self.album_title)  # debug

        self.json_imageIDs = list(self._init_image_ids_with_json(html=html))
        self.imageIDs = self.json_imageIDs

        if self.debug:
            print("imageIDs count: %s" % str(len(self.imageIDs)))  # debug
            print("imageIDs:\n%s" % str(self.imageIDs))  # debug

        self.extension_counter = Counter()
        for i in self.imageIDs:
            self.extension_counter[i[1]] += 1

    @staticmethod
    def get_all_format_url(album_url):
        """get `all` format url from album url."""
        parsed_url = urlparse(album_url)
        if not parsed_url.path.startswith(('/a/', '/gallery/')):
            return album_url
        album_id = parsed_url.path.split('/')[2]
        # e.g.:  ['', 'a', 'p5wLR']
        # e.g.:  ['', 'gallery', 'p5wLR']
        new_path = '/a/{}/all'.format(album_id)
        return parsed_url._replace(path=new_path).geturl()

    def _init_image_ids_with_json(self, html):
        """get html section that contains image ID(s) and file extensions of 
        each ID with json."""
        """Format of the search variable.
        item: <java dict>\n};
        """
        image_ids = None
        search = re.search('(item:.*?};)', html, flags=re.DOTALL)
        if not search:
            raise Exception("Failed to find regex match in html")
        try:
            search = search.group().replace('\n', '', ).split(':', 1)[1].rsplit('}', 1)[0]
            json_search = json.loads(search)
            if 'album_images' in json_search:
                img_dicts = json_search['album_images']['images']
                for img_dict in img_dicts:
                    # ext can be either '.jpg' or '.jpg?1'
                    ext = img_dict['ext']
                    ext = ext.split('?')[0] if '?' in ext else ext
                    yield (img_dict['hash'], ext)
            elif 'hash' in json_search:
                # safe guard if any '?' in ext
                ext = json_search['ext']
                ext = ext.split('?')[0] if '?' in ext else ext
                yield (json_search['hash'], ext)
            else:
                self.log.debug('Unknown json search key: {}'.format(json_search))
        except Exception as e:
            raise Exception('JSON parse failed: {}'.format(e))

        if image_ids:
            yield image_ids

    def _init_image_ids_with_regex(self, html):
        """get section from html that contains image ID(s) and file extensions 
        of each ID.
        """
        image_ids = None
        search = re.search('(item:.*?};)', html, flags=re.DOTALL)
        if search:
            # this'll fix those albums with one picture
            if '"count"' in search.group(0):
                search = re.search('"images".*?]', search.group(0), flags=re.DOTALL)
            image_ids = re.findall(
                '.*?"hash":"([a-zA-Z0-9]+)".*?"ext":"(\.[a-zA-Z0-9]+)".*?',
                search.group(0))
            # removes the 1st element in imageIDs
            # since this'll be the main_key if this link has more than 1 img
            if len(image_ids) > 1 and image_ids[0][0] == self.main_key:
                image_ids.remove(image_ids[0])
        else:
            raise Exception("Failed to find regex match in html")
        return image_ids

    def num_images(self):
        """
        Returns the number of images that are present in this album.
        """
        return len(self.imageIDs)

    def list_extensions(self):
        """
        Returns list with occurrences of extensions in descending order.
        """
        if hasattr(self, "extension_counter"):
            if self.extension_counter:
                return self.extension_counter.most_common()

    def get_album_key(self):
        """
        Returns the key of this album. Helpful if you plan on generating your 
        own folder names.
        """
        return self.main_key

    def on_image_download(self, callback):
        """
        Allows you to bind a function that will be called just before an image
        is about to be downloaded. You'll be given the 1-indexed position of 
        the image, it's URL and it's destination file in the callback like so:
            my_awesome_callback(1, "http://i.imgur.com/fGWX0.jpg", "~/Downloads/1-fGWX0.jpg")
        """
        self.image_callbacks.append(callback)

    def on_complete(self, callback):
        """
        Allows you to bind onto the end of the process,
        displaying any lovely messages
        to your users, or carrying on with the rest of the program. Whichever.
        """
        self.complete_callbacks.append(callback)

    def save_images(self, folder_name=''):
        """
        Saves the images from the album into a folder given by foldername.
        If no foldername is given, it'll use the cwd and the album key.
        And if the folder doesn't exist, it'll try and create it.

        :param folder_name: string that describes the (base) name of the folder
            in which the image(s) are saved in (does not include full path)
        :return: final filenames of each file successfully downloaded, numb of
            images skipped

        """
        # Try and create the album folder:
        album_folder = '' if not folder_name else folder_name
        if len(self.imageIDs) > 1:
            album_folder = self.album_title

        dir_save = os.path.join(self.dir_download, album_folder)
        downloaded = skipped = 0

        if not os.path.exists(dir_save):
            os.makedirs(dir_save)

        final_filenames = []
        # And finally loop through and save the images:
        for (counter, image) in enumerate(self.imageIDs, start=1):
            key = image[0]
            ext = image[1]
            # should be safe to save & open as .mp4
            if ext.endswith(('.gifv', 'gif')):
                ext = '.mp4'
                # image_url, ext = get_gifv_info(image_url, key, ext)
                # print('img_url: %s \next: %s' % (image_url, ext))

            image_url = "http://i.imgur.com/" + key + ext

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

            # download url content into file that path points to, slugifying
            # file name of path
            dl, skp = self.direct_download(
                image_url,
                os.path.join(
                    os.path.dirname(path),
                    slugify(os.path.basename(path))))

            downloaded += dl
            skipped += skipped
            if dl != 0:
                final_filenames.append(filename)

        # Run the complete callbacks:
        for fn in self.complete_callbacks:
            fn()

        # return downloaded, skipped, final_filenames
        return final_filenames, skipped

    def direct_download(self, image_url, path):
        """download data from url and save to path
            & optionally check if img downloaded is imgur dne file
        """

        def are_files_equal(file1, file2):
            """given two file objects, check to see if their bytes are equal"""
            return True if bytearray(file1.read()) == bytearray(file2.read()) \
                else False

        dl, skp = 0, 0
        if os.path.isfile(path):
            raise FileExistsException(
                '%s already exists.' % os.path.basename(path))
        else:
            try:
                request = urllib.request.urlopen(image_url)
                redirect_url = request.geturl()

                # check if image did not exist and url got redirected
                if image_url != redirect_url:
                    self.log.debug('url, redirected_url = %s, %s'
                                   % (image_url, redirect_url))
                    if redirect_url == 'http://imgur.com/':
                        raise HTTPError(
                            404, "Image redirected to non-image link",
                            redirect_url, None, None)

                # check if image is imgur dne image before we download anything
                if self.delete_dne:
                    try:
                        with open(self.dne_path, 'rb') as dne_file:
                            if are_files_equal(request, dne_file):
                                if self.debug:
                                    print('[ImgurDownloader] DNE: %s' %
                                          path.split('/')[-1])
                                return 0, 1
                    except (FileNotFoundError, OSError):
                        if self.debug:
                            print('[ImgurDownloader] Warning: DNE image not '
                                  'found at {}'.format(self.dne_path))

                # proceed with downloading
                urllib.request.urlretrieve(image_url, path)
                dl = 1
            except (HTTPError, FileExistsError):
                skp = 1
        return dl, skp

    def is_imgur_dne_image(self, img_path):
        """takes full image path & checks it.

        It will check if bytes are equal to that of imgur does not exist image.
        """
        # edit location if needed
        dne_img = os.path.join(self.dir_root, 'imgur-dne.png')
        with open(dne_img, 'rb') as f:
            dne_data = bytearray(f.read())
        with open(img_path, 'rb') as f:
            data = bytearray(f.read())
        return True if data == dne_data else False


def slugify(value):
    """Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    # taken from http://stackoverflow.com/a/295466
    # with some modification
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = str(re.sub(r'[^\w\s\-.)(]', '', value.decode('ascii')).strip())
    return value


@click.command()
@click.option(
    '--print-only', default=False, is_flag=True,
    help="Print download link only, no download.")
@click.argument('url', nargs=1, required=False)
@click.argument('destination_folder', nargs=1, required=False)
def main(url, destination_folder, print_only=False):
    """Quickly and easily download images from Imgur."""
    if not url:
        # Print out the help message and exit:
        print(__doc__)
        exit()

    try:
        # Fire up the class:
        downloader = ImgurDownloader(url)

        if not print_only:
            print(("Found {0} images in album"
                   .format(downloader.num_images())))

            exts = downloader.list_extensions()
            if exts is not None:
                for i in exts:
                    print(("Found {0} files with {1} extension"
                           .format(i[1], i[0])))

        # Called when an image is about to download:
        def print_image_progress(index, url, dest):
            print(("Downloading Image %d" % index))
            print(("    %s >> %s" % (url, dest)))

        downloader.on_image_download(print_image_progress)

        # Called when the downloads are all done.
        def all_done():
            print("")
            print("Done!")

        downloader.on_complete(all_done)

        # Work out if we have a foldername or not:
        if destination_folder:
            albumFolder = destination_folder
        else:
            albumFolder = ''

        if not print_only:
            # Enough talk, let's save!
            downloader.save_images(albumFolder)
        else:
            # for img_id, ext in downloader.json_imageIDs:
            for img_id, ext in downloader.imageIDs:
                print('https://i.imgur.com/{}{}'.format(img_id, ext))
        exit()  # NOTE: may not be needed

    except ImgurException as e:
        print(("Error: " + e.msg))
        print("")
        print("How to use")
        print("=============")
        print(__doc__)
        exit(1)


if __name__ == '__main__':
    main()
