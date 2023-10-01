================
Imgur Downloader
================

Deprecated in favor of gallery-dl (https://github.com/mikf/gallery-dl/tree/master)

------

Check for support for this there or report an issue there.

This is a simple Python script that contains a class and command line interface
that allows you to download ann images at full resolution with any imgur link, all at once.

jtara1 Fork - Features
----------------------

- Here's some examples of the types of links that are now supported:

 - http://imgur.com/FVRUGe2
 - http://imgur.com/FVRUGe2.jpg
 - http://imgur.com/gallery/LHCvGPA
 - http://imgur.com/r/awwnime/W7N6A
 - http://i.imgur.com/j9W9tSi.jpg
 - http://imgur.com/a/SVq41
 - http://i.imgur.com/A61SaA1.gifv

- Name of album folder or image is determined by HTML `<title>` value or passed parameters.
- Prevents downloading of Imgur `Does Not Exist` image
  by checking if direct link url got redirected & comparing the bytearrays of the direct link image with that of a local file.
- Uses album/gallery/image title as folder title that's created and contains image(s) with key appended e.g.::

    We don't have a blue backdrop, just tint the whole photo blue. (SnkkAVU).png

- Add `--print-only` option to print the direct link of the imgur url.
- Prevents downloading of imgur does not exist image if it is encountered.
  It is implemented by comparing the bytes of the HTTP request
  to that of a local imgur dne file in program.
  This feature is toggleable in `init` parameter.

 - Added function `is_imgur_dne_image(self, img_path)`,
   which returns `True`
   if the image from `img_path` is the same image as the Imgur does not exist image
   and return `False` otherwise.

 - Added function `are_files_equal(self, file1, file2)`,
   which compares the bytes and returns `True` if the bytes are equal, and return `False` otherwise

.. code:: python

 ImgurDownloader(
     'http://i.imgur.com/removed.png', delete_dne=True, debug=True
 ).save_images()

- Downloads imgur links with .gifv extension as a mp4 file

.. code:: python

 ImgurDownloader('http://i.imgur.com/A61SaA1.gifv').save_images()

* `save_images` & `direct_download` methods now return tuple of two integers.
  The first integer represent successful downloads
  and the second represent skipped download (either failed or Imgur DNE detected).
  For example the value on the the last line of the output is what's returned from `save_images` method:

.. code:: python

 # Code ran (url is an imgur Album with 5 images):
 print(
     imguralbum.ImgurDownloader(
         url, dir1, file_name=rand_name, debug=False
     ).save_images()
 )
 # output: (5, 0)


Init function parameter changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Second optional parameter, `dir_download=os.getcwd()`,
  which allows for specific directory to download to (not adapted for cli), e.g.:

.. code:: python

 ImgurDownloader('http://imgur.com/SnkkAVU', '/home/user/Downloads/')

- Third optional parameter, `file_name=''`,
  which allows user to specify name of file if input is single image
  or folder if input is album.
  Note this takes priority over the imgur key and the album webpage title e.g.:

.. code:: python

 ImgurDownloader(
     'http://imgur.com/SnkkAVU', '/home/user/Downloads/', 'my-img')

- Fourth optional parameter, `delete_dne=True`,
  which checks each image downloaded and deletes it if its bytes match that of imgur-dne.png, e.g.:

.. code:: python

 ImgurDownloader(
     'http://imgur.com/SnkkAVU', '/home/user/Downloads/', 'my-img', True)

- Fifth optional parameter, debug=False,
  which prints a number of variables throughout the code as it runs

.. code:: python

 ImgurDownloader(
     'http://imgur.com/SnkkAVU', '/home/user/Downloads/', 'my-img', True, True)


Requirements
------------

Python >= 3.3

Command Line Usage
------------------

.. code:: bash

 $ imgur_downloader [album URL] [folder to save to]

Download all images from an album into the folder /Users/alex/images/downloaded

.. code:: bash

 $ imgur_downloader http://imgur.com/a/uOOju /Users/alex/images/downloaded

Downloads all images and puts them into an album in the current directory called "uOOju"

.. code:: bash

 $ imgur_downloader http://imgur.com/a/uOOju


It can also be used with downloader such as `wget` using `--print-only` option.

.. code:: bash

 $ imgur_downloader --print-only http://imgur.com/a/SVq41 | xargs wget


Class Usage
-----------

The class allows you to download imgur albums in your own Python programs without going
through the command line. Here's an example of it's usage:

.. code:: python

 downloader = ImgurDownloader("http://imgur.com/a/uOOju")
 print("This albums has {} images".format(downloader.num_images()))
 downloader.save_images()

Callbacks
^^^^^^^^^

You can hook into the classes process through a couple of callbacks:

.. code:: python

 downloader.on_image_download()
 downloader.on_complete()

You can see what params and such your callback functions get by looking at the docblocks
for the on_* functions in the .py file.

Full docs
---------

The whole shebang, class and CLI is fully documented using string-docblock things in the single .py file
so please read through that rather than rely on this readme which could drift out of date.

License
-------

MIT

Credits
-------

Originally written by `Alex Gisby`_ (`@alexgisby`_)

With `Contributions from these amazing people`_!)

.. _Alex Gisby: https://github.com/alexgisby
.. _@alexgisby: http://twitter.com/alexgisby
.. _Contributions from these amazing people: https://github.com/jtara1/imgur-downloader/graphs/contributors
