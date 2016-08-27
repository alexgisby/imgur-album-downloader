# imgur Album Downloader

This is a simple Python script that contains a class and command line interface that
allows you to download ann images at full resolution in an imgur album, all at once.

## jtara1 Fork - Features
Features added:

* supports imgur images that aren't "gallery" or "a" or "album" e.g.:

>http://imgur.com/SnkkAVU

>http://i.imgur.com/SnkkAVU.png

* uses album/gallery/image title as folder title that's created and contains image(s) with key appended e.g.:

>We don't have a blue backdrop, just tint the whole photo blue. (SnkkAVU)

* \_\_init\_\_ function of ImgurAlbumDownloader takes an 2nd (optional) parameter, dir_download=os.getcwd(), which allows for specific directory to download to (not adapted for cli), e.g.:

>downloader = ImgurAlbumDownloader('http://imgur.com/SnkkAVU', '/home/user/Downloads/')

* \_\_init\_\_ function of ImgurAlbumDownloader takes a 3rd (optional) parameter, file_name='', which allows user to specify name of file or folder that's being downloaded from imgur url (will be name of folder if album else will be file name if downloading single img). Note this takes priority over the imgur key and the album title search.

>downloader = ImgurAlbumDownloader('http://imgur.com/SnkkAVU', '/home/user/Downloads/', 'my-img')

* \_\_init\_\_ function of ImgurAlbumDownloaders takes a 4th (optional) parameter, debug=False, which prints a number of variables throughout the code as it runs

>downloader = ImgurAlbumDownloader('http://imgur.com/SnkkAVU', '/home/user/Downloads/', 'my-img', True)

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
	downloader = ImgurAlbumDownloader("http://imgur.com/a/uOOju")
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

With [Contributions from these amazing people!](https://github.com/alexgisby/imgur-album-downloader/graphs/contributors)
