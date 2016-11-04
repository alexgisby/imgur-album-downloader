# Imgur Downloader

This is a simple Python script that contains a class and command line interface that
allows you to download ann images at full resolution with any imgur link, all at once.

## jtara1 Fork - Features

**tl;dl comparison of my fork & original repo**

- Here's some examples of the types of links that are now supported:

      http://imgur.com/FVRUGe2

      http://imgur.com/gallery/LHCvGPA

      http://imgur.com/r/awwnime/W7N6A

      http://i.imgur.com/j9W9tSi.jpg

      http://imgur.com/a/SVq41

      http://i.imgur.com/A61SaA1.gifv


- Name of album folder or image is determined by HTML `<title>` value or parameters passed
- Prevents downloading of Imgur Does Not Exist image (by checking if direct link url got redirected & comparing the bytearrays of the direct link image with that of a local file).

---

Features added:

* supports imgur images that aren't "gallery" or "a" or "album" e.g.:

    >http://imgur.com/SnkkAVU

    >http://i.imgur.com/SnkkAVU.png

* uses album/gallery/image title as folder title that's created and contains image(s) with key appended e.g.:

    >We don't have a blue backdrop, just tint the whole photo blue. (SnkkAVU).png

* prevents downloading of imgur does not exist image if it is encountered (now toggleable by \_\_init\_\_ parameter) implemented by comparing the bytes of the HTTP request to that of a local imgur dne file in  self.direct_download(...)

    * added function is\_imgur\_dne\_image(self, img\_path) which returns True if the image from img\_path is the same image as the Imgur does not exist image false otherwise

    * added function are\_files\_equal(self, file1, file2) which compares the bytes and returns True if the bytes are equal, False otherwise

            ImgurDownloader('http://i.imgur.com/removed.png', delete_dne=True, debug=True).save_images()

* downloads imgur links with .gifv extension as a
~~.webm~~ ~~.gif~~ .mp4 file

        ImgurDownloader('http://i.imgur.com/A61SaA1.gifv').save_images()

* save_images & direct_download methods now return tuple of two integers, the first representing successful downloads and the second representing skipped download (either failed or Imgur DNE detected) example, the value on the the last line of the output is what's returned from save_images method

    Code ran (url1 is an Imugr Album with 5 images):

            print(imguralbum.ImgurDownloader(url1, dir1, file_name=rand_name, debug=False).save_images())

    Printed output:

        (5, 0)

* supports links associated with a subreddit (thanks for the tip [rachmadaniHaryono](https://github.com/rachmadaniHaryono))

        ImgurDownloader('http://imgur.com/r/awwnime/W7N6A').save_images()

#### \_\_init\_\_ function parameter changes:

* \_\_init\_\_ function of ImgurDownloader takes an 2nd (optional) parameter, dir_download=os.getcwd(), which allows for specific directory to download to (not adapted for cli), e.g.:

        downloader = ImgurDownloader('http://imgur.com/SnkkAVU', '/home/user/Downloads/')

* \_\_init\_\_ function of ImgurDownloader takes a 3rd (optional) parameter, file_name='', which allows user to specify name of file or folder that's being downloaded from imgur url (will be name of folder if album else will be file name if downloading single img). Note this takes priority over the imgur key and the album webpage title.

        downloader = ImgurDownloader('http://imgur.com/SnkkAVU', '/home/user/Downloads/', 'my-img')

* \_\_init\_\_ function of ImgurDownloader takes a 4th (optional) parameter, delete_dne=True, which checks each
image downloaded and deletes it if its bytes match that of imgur-dne.png

        downloader = ImgurDownloader('http://imgur.com/SnkkAVU', '/home/user/Downloads/', 'my-img', True)

* \_\_init\_\_ function of ImgurDownloader takes a 5th (optional) parameter, debug=False, which prints a number of variables throughout the code as it runs

        downloader = ImgurDownloader('http://imgur.com/SnkkAVU', '/home/user/Downloads/', 'my-img', True, True)


## Requirements

Python >= 3.3

## Command Line Usage

	$ python3 imguralbum.py [album URL] [folder to save to]

Download all images from an album into the folder /Users/alex/images/downloaded

	$ python3 imguralbum.py http://imgur.com/a/uOOju /Users/alex/images/downloaded

Downloads all images and puts them into an album in the current directory called "uOOju"

	$ python3 imguralbum.py http://imgur.com/a/uOOju


## Class Usage

The class allows you to download imgur albums in your own Python programs without going
through the command line. Here's an example of it's usage:

### Example:
	downloader = ImgurDownloader("http://imgur.com/a/uOOju")
	print "This albums has %d images" % downloader.num_images()
	downloader.save_images()

### Callbacks:
You can hook into the classes process through a couple of callbacks:

	downloader.on_image_download()
	downloader.on_complete()

You can see what params and such your callback functions get by looking at the docblocks
for the on_XXX functions in the .py file.

## Full docs:

The whole shebang, class and CLI is fully documented using string-docblock things in the single .py file
so please read through that rather than rely on this readme which could drift out of date.

## License

MIT

## Credits

Originally written by [Alex Gisby](https://github.com/alexgisby) ([@alexgisby](http://twitter.com/alexgisby))

With [Contributions from these amazing people!](https://github.com/jtara1/imgur-downloader/graphs/contributors)
