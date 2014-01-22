#!/usr/bin/env python

import os
import sys
from setuptools import setup

sys.path.insert(0, os.path.abspath('griotte/lib'))
from griotte import __version__, __author__

def get_data_files():
    files = os.popen("git ls-files static").read().split('\n')[0:-1]
    df = {}
    final = []
    for f in files:
        directory = f[0:f.rfind('/')]
        if directory in df:
            df[directory].append(f)
        else:
            df[directory] = [f]
    for k in df:
        final.append(("/usr/local/share/griotte/" + k, df[k]))
    return final

setup(name='griotte',
      version=__version__,
      description='Museum Media Player',
      long_description='',
      author=__author__,
      author_email='mblanc@erasme.org',
      url='http://griotte.erasme.org/',
      license='GPLv3',
      dependency_links = [
         'https://github.com/liris/websocket-client/tarball/py3#egg=websocket-client-0.12.0',
         #'https://github.com/quick2wire/quick2wire-python-api/tarball/master#egg=quick2wire-python-api-0.0.0.2'
         ],
      install_requires=['RPIO', 'websocket-client-py3', 'tornado', 'setproctitle'],
      package_dir={ 'griotte': 'griotte/lib/griotte' },
      tests_require=['nose'],
      packages=[ 'griotte',
                 'griotte.adc',
                 'griotte.gpio',
                 'griotte.multimedia',
                 'griotte.scenario',
                 'griotte.server',
                 'griotte.ws' ],
      scripts=[
         'griotte/bin/adc',
         'griotte/bin/gpio',
         'griotte/bin/multimedia',
         'griotte/bin/server',
         'griotte/bin/storage',
      ],
#      data_files=glob('./static/**/**')
      data_files= [ get_data_files(),
                    ('/etc/init.d/', ['griotte/config/griotte.init'],
                     '/etc/griotte.conf', ['griotte/config/griotte.conf'],)
)

# pip install -e git://github.com/liris/websocket-client@py3#egg=websocket-client
# pip install -e git://github.com/quick2wire/quick2wire-python-api@master#egg=quick2wire-python-api
