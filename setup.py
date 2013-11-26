#!/usr/bin/env python

import os
import sys
from glob import glob

sys.path.insert(0, os.path.abspath('lib'))
from raspeomix import __version__, __author__
from distutils.core import setup

setup(name='raspeomix',
      version=__version__,
      description='Museum Media Player',
      author=__author__,
      author_email='mblanc@erasme.org',
      url='http://ansibleworks.com/',
      license='GPLv3',
      install_requires=['RPIO', 'websocket'],
      package_dir={ 'raspeomix': 'lib/raspeomix' },
      packages=[
         'raspeomix',
         'raspeomix.websocket',
         'raspeomix.gpio',
      ],
      scripts=[
         'bin/gpio',
         'bin/analog',
         'bin/server',
      ],
      data_files=glob('./static/**/*')
)
