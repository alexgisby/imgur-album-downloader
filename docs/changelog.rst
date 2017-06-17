Changelog
=========

0.1.0 (unreleased)
------------------

New
~~~

- Add `__init__.py` for tests folder so unit tests can run properly using pytest. [jtara1]
- Add unit tests, now tests most common imgur links. [jtara1]
- Add test py file for pytest. [jtara1]
- Add checking for redirect DNE image, some debug logging, & fix bytearray compare DNE checking. [James T]
- Supports `/r/` links (subreddit categorized) [James T]
- Add imgur-dne (png) image as reference. [James T]
- Add file_name arg to __init__(...) & added args desc to docstring.  [James T]
- Add optional param in __init__ for debug and dir. [James T]
- Add support for downlading files with various extensions [Szero]]
- Add deletion of files if the download fails. [Szero]
- Add method that counts up extensions.  [Szero]
- Add support for downlading files with various extensions. [Szero]
- Add support for gallery URLs. [Philip Huppert]
- Add support for imgur's new ?1 style urls (fixes #13). [Alex Gisby]
- Made support for 3.4. [polyx]
- Add support for https. [Lemuel Formacil]
- Prefix the filename with a sequence number. [Lemuel Formacil]
- Add support for non jpeg files. [Alex Gisby]
- Add license and readme. [Alex Gisby]

Fix
~~~

- Fix single img id parsing [jtara1]
- .gifv saves as .mp4 now, should work with all .gifv link. [James T]
- Direct_download method returns amount downloaded & skipped in every case. [James T]
- Albums with single image (long time bug), direct_download func now raises exceptions. [James T]
- Imgur DNE download prevention works. [James T]
- Regex for gallery links, & albums w/ 1 img w/ author. [James T]
- Fix dne_file failing to close  when exception was raised. [James T]
- DNE checker no longer removes valid images from albums.  [James T]
- DNE deletion in self.urlretrieve_hook(...) works now.  [James T]
- Img dne checker works with ALL imgs, renamed classes. [James T]
- Fix direct link dl. [James T]
- Fix support for older albums that don't have ?1 style image URLs.  [Alex Gisby]
- Fix display of image counts and updating readme. [Alex Gisby]

Change
~~~~~~

- Change files to pass flake8 test. [rachmadaniHaryono]
- Use Restructured text instead of Markdown file for readme.
- All .gif files are saved as .mp4, [James T]
- List of final downloaded filenames returned instead of number of successful downloads in save_images method. [James T]
- Update new Exception class, FileExists. [James T]
- Rename main file to reflect function. [James T]
- `save_images` & `direct_download` funcs return tuple of number of successful downloads & skipped downloads. [James T]
- Obtain `imgur_dne.png` by opening from directory of `imguralbum.py` file. [James T]
- Cleanup direct_download(...) param. [James T]
- Update imgur dne image name. [James T]
- Update self.remove_extension(...) [James T]
- Update dne checker feature to be more efficient for big albums. [James T]
- Rename function isImgurDneImage(...) to ImgurAlbumDownloader class.  [James T]
- __init__(...) param file_name takes 1st priority for file/folder name
- Single img now saves to root instead of new folder. [James T]
- Simplified the regex [Szero]
- Adjusted regex. [Szero]
- Use python3 explicitely. [nodiscc]
- Specify that we want python3. [Robin Appelman]
- Using full-res rather than hi-res. #17. [Alex Gisby]
- Changing to use the blogs layout rather than noscript. [Alex Gisby]
- Skip files that are already downloaded. [O. R. Lissenberg]
- Allow mobile links to be valid. [Danny]
- Refactored the downloader class to use callbacks instead of printing stuff internally. [Alex Gisby]
- Allow for hi-res images to be downloaded (fixes #5). [Alex Gisby]
- Remove 'http:' in `src` attr of `img` tag. [Lemuel Formacil]
- Clean up file to adhere to the PEP8 style guide. [Lemuel Formacil]
- Exit with a non-zero error code on exceptions. [Vikraman Choudhury]
- Refactored into a sexy class type thing. [Alex Gisby]

Other
~~~~~

- Initial commit, works well enough. [Alex Gisby]
