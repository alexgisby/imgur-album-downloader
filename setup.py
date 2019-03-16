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
directory = dirname(abspath(__file__))
# get module name from parent folder name
# assumes the parent folder (repository name) is the same as the module name
module_name = basename(directory)

description = 'Python script/class to download an entire Imgur album in ' \
              ' one go into a folder of your choice'


def create_setup_cfg(callback=None):
    """Creates the setup.cfg file with basic metadata and calls the callback"""
    with open(join(directory, 'setup.cfg'), 'w') as config:
        config.write(
            "[metadata]\nname = {module_name}\ndescription-file = {file_name}"
            .format(module_name=module_name, file_name=readme_file_name))
    if callback is not None:
        callback()


def change_rst_to_md_extension_in_cfg():
    """Replaces README.rst with README.md in setup.cfg"""
    try:
        with open(join(directory, 'setup.cfg'), 'r+') as config:
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
    with open(join(directory, 'README.rst')) as f:
        readme_file_name = 'README.rst'
        readme = f.read()
except (FileNotFoundError, FileExistsError):
    try:
        with open(join(directory, 'README.md')) as f:
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
        with open(join(directory, 'requirements.txt'), 'r') as req_file:
            for line in req_file:
                requirements.append(re.sub("\s", "", line))
    except (FileExistsError, FileNotFoundError):
        print('[setup.py] Note: No requirements.txt found')
    return requirements


def update_cfg_module_name():
    """Replaces the module name in setup.cfg with module_name"""
    try:
        with open(join(directory, 'setup.cfg'), 'r+') as config:
            text = config.read()
            text = re.sub('name = module_name(_setup_cfg)?',
                          'name = {}'.format(module_name),
                          text)
            config.seek(0)
            config.truncate()
            config.write(text)
    except (FileNotFoundError, FileExistsError):
        create_setup_cfg(update_cfg_module_name)
        # print('[setup.py] Warning: No setup.cfg found')


update_cfg_module_name()

setup(use_scm_version={'root': directory},
      setup_requires=['setuptools_scm'],
      name=module_name,
      packages=find_packages(),  # find all dependencies for this module
      # version=version,
      description=description,
      long_description=readme,
      license='MIT',
      author='Alex Gisby',
      author_email='alex@solution10.com',
      url='https://github.com/jtara1/imgur_downloader',
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
