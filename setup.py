from setuptools import setup, find_packages
import re
from os.path import join, dirname, basename, abspath


__doc__ = """This template setup.py file was intended to be generic enough
for use in any of my python modules on github. It will create setup.cfg and  
update the metadata that is required there. It'll automatically determine the 
name of the module by using the parent folder name of this setup.py file.
It pulls the text inside the README.md or README.rst to use in the 
long_descriptiion of the setup function
Fill out the information below with your own for your module.
The version 

Author: https://github.com/jtara1
Source: 
https://github.com/jtara1/misc_scripts/blob/master/misc_scripts/templates/setup.py
"""

# path to this file but not including this file
__path = dirname(abspath(__file__))
# get module name from parent folder name
# assumes the parent folder (repository name) is the same as the module name
module_name = basename(__path)


def get_version_from_init():
    with open(join(__path, module_name, '__init__.py'), 'r') as init:
        match = re.search("__version__\s*=\s*'([\w.-]+)'", init.read())
    return match.group(1) if match is not None else None

# attempt to find variable module_name.__init__.__version__
__version__ = None
try:
    __version__ = get_version_from_init()
    if __version__ is None:
        print('[setup.py] Note: There was no __version__ variable within the '
              '__init__.py of the {}'.format(module_name))
    else:
        print('[setup.py] grabbed __version__ of {0} from {0}/__init__.py'
              .format(module_name))
except (FileExistsError, FileNotFoundError) as e:
    print(type(e), e)
    print('[setup.py] Note: There was no __init__.py found within {}'
          .format(module_name))


# -------------- Update the following variables --------------- #
# prioritize using __version__ in module_name.__init__ if it's there
version = '0.1.0' if __version__ is None else __version__
description = 'Python script/class to download an entire Imgur album in ' \
              ' one go into a folder of your choice'
# ------------------------------------------------------------- #


def create_setup_cfg(callback=None):
    """Creates the setup.cfg file with basic metadata and calls the callback"""
    with open(join(__path, 'setup.cfg'), 'w') as config:
        config.write(
            "[metadata]\nname = {module_name}\ndescription-file = {file_name}"
            .format(module_name=module_name, file_name=readme_file_name))
    if callback is not None:
        callback()


def change_rst_to_md_extension_in_cfg():
    """Replaces README.rst with README.md in setup.cfg"""
    try:
        with open(join(__path, 'setup.cfg'), 'r+') as config:
            text = config.read()
            text = re.sub('README.rst', 'README.md', text)
            config.seek(0)
            config.write(text)
    except (FileNotFoundError, FileExistsError):
        create_setup_cfg(change_rst_to_md_extension_in_cfg)
        # print('[setup.py] Warning: No setup.cfg found')


# Store text from README.rst or README.md to use in long description and
# update setup.cfg to point to the correct readme if needed
try:
    with open(join(__path, 'README.rst')) as f:
        readme_file_name = 'README.rst'
        readme = f.read()
except (FileNotFoundError, FileExistsError):
    try:
        with open(join(__path, 'README.md')) as f:
            readme_file_name = 'README.md'
            readme = f.read()
            change_rst_to_md_extension_in_cfg()
    except (FileExistsError, FileNotFoundError):
        readme = description


def get_install_requirements():
    """Returns the parsed list of strings of required modules listed in
    requirements.txt"""
    requirements = []
    try:
        with open(join(__path, 'requirements.txt'), 'r') as req_file:
            for line in req_file:
                requirements.append(re.sub("\s", "", line))
    except (FileExistsError, FileNotFoundError):
        print('[setup.py] Note: No requirements.txt found')
    return requirements


def update_cfg_module_name():
    """Replaces the module name in setup.cfg with module_name"""
    try:
        with open(join(__path, 'setup.cfg'), 'r+') as config:
            text = config.read()
            text = re.sub('name = module_name(_setup_cfg)?',
                          'name = {}'.format(module_name),
                          text)
            config.seek(0)
            config.write(text)
    except (FileNotFoundError, FileExistsError):
        create_setup_cfg(update_cfg_module_name)
        # print('[setup.py] Warning: No setup.cfg found')


update_cfg_module_name()

setup(name=module_name,
      packages=find_packages(),  # find all dependencies for this module
      version=version,
      description=description,
      long_description=readme,
      license='MIT',
      author='Alex Gisby',
      author_email='alex@solution10.com',
      url='https://github.com/jtara1/imgur_downloader',
      download_url='{github_url}/archive/{version}.tar.gz' \
      .format(github_url='https://github.com/jtara1/imgur_downloader',
              version=version),
      keywords=['imgur', 'downloader'],
      maintainer='jtara1',  #'rachmadaniHaryon',
      install_requires=get_install_requirements(),
      # list of strs https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.5",
      ],
      zip_safe=False,
      entry_points={
          'console_scripts':
              ['imgur_downloader=imgur_downloader.__main__:main']}
      )
