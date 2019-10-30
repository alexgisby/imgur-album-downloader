# imgur Album Downloader

This is a simple Python script that contains a class and command line interface that
allows you to download ann images at full resolution in an imgur album, all at once.

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

With [Contributions from these amazing people!](https://github.com/alexgisby/imgur-album-downloader/graphs/contributors)
