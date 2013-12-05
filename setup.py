#!/usr/bin/env python

import os
import sys
from glob import glob
from setuptools import setup

sys.path.insert(0, os.path.abspath('lib'))
from raspeomix import __version__, __author__

setup(name='raspeomix',
      version=__version__,
      description='Museum Media Player',
      author=__author__,
      author_email='mblanc@erasme.org',
      url='http://ansibleworks.com/',
      license='GPLv3',
      dependency_links = [
         #'https://github.com/liris/websocket-client/tarball/py3#egg=websocket-client-0.12.0',
         'https://github.com/quick2wire/quick2wire-python-api/tarball/master#egg=quick2wire-python-api-0.0.0.2' ],
      install_requires=['RPIO', 'websocket-client-py3', 'tornado', 'quick2wire_api'],
      package_dir={ 'raspeomix': 'lib/raspeomix' },
      tests_require=['nose'],
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

# pip install -e git://github.com/liris/websocket-client@py3#egg=websocket-client
# pip install -e git://github.com/quick2wire/quick2wire-python-api@master#egg=quick2wire-python-api
