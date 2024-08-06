#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

from version import __version__

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = ['evrhash']

setup(name='python-evrmorelib',
      version=__version__,
      description='Evrmore fork of python-bitcoinlib',
      long_description=README,
      long_description_content_type='text/markdown',
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
      ],
      url='https://github.com/EvrmoreOrg/python-evrmorelib',
      keywords='evrmore',
      packages=find_packages(),
      zip_safe=False,
      author = 'EvrmoreOrg',
      author_email = '',
      install_requires=requires,
      test_suite="evrmore.tests"
     )
