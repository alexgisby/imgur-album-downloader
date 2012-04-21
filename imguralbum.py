#!/usr/bin/env python
# encoding: utf-8
"""
imguralbum.py

MIT License

"""

import sys
import re
import urllib
import os

help_message = '''

Quickly and easily download an album from Imgur.

Format:
	python imguralbum.py [album URL] [destination folder]
	
Example:
	python imguralbum.py http://imgur.com/a/uOOju#6 images
	
If you omit the dest folder name, the utility will create one with the same name as the
album (for example for http://imgur.com/a/uOOju it'll create uOOju/ in the cwd)

'''

class ImgurAlbumException(Exception):
	def __init__(self, msg):
		print msg

args = sys.argv

if len(args) == 1:
	raise ImgurAlbumException("You must provide the album URL")

albumURL = args[1]

# Check the URL is actually imgur:
match = re.match('http\:\/\/(www\.)?imgur\.com/a/([a-zA-Z0-9]+)(#[0-9]+)?', albumURL)
if not match:
	raise ImgurAlbumException("URL must be a valid Imgur Album")

print "Reading Album: " + albumURL

# We read from the noscript version of imgur to make sure all images are on the page:
noscriptURL = 'http://imgur.com/a/' + match.group(2) + '/noscript'
response = urllib.urlopen(noscriptURL)

if response.getcode() != 200:
	raise ImgurAlbumException("Error reading Imgur: %d" % response.getcode())

print "Album found!"

html = response.read()
images = re.findall('<img src="(http\:\/\/i\.imgur\.com\/([a-zA-Z0-9]+\.(jpg|jpeg|png|gif)))"', html)

print "Found %d images in album" % len(images)

# Try and create the album folder:
if len(args) == 3:
	albumFolder = args[2] 
else:
	albumFolder = match.group(2)

if not os.path.exists(albumFolder):
	os.makedirs(albumFolder)

# And finally loop through and save the images:
for image in images:
	print "Fetching Image: " + image[0]
	path = os.path.join(albumFolder, image[1])
	urllib.urlretrieve(image[0], path)

print ""
print "All done!"