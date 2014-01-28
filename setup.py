#!/usr/bin/env python

import os
import sys
from setuptools import setup
from pprint import pprint

sys.path.insert(0, os.path.abspath('griotte/lib'))
from griotte import __version__, __author__

def get_data_files():
    df = {}
    final = []
    for root, dirs, files in os.walk("static", topdown=False):
        for name in files:
            if root in df:
                df[root].append("%s/%s" % (root, name))
            else:
                df[root] = ["%s/%s" % (root, name)]
    for k in df:
        final.append(("/usr/local/share/griotte/static/%s" % k, df[k]))
    pprint(final)
    return final

def gen_data_files(*dirs):
    results = []

    for src_dir in dirs:
        for root,dirs,files in os.walk(src_dir):
            #results.append((root, map(lambda f:root + "/" + f, files)))
            results.append(("/usr/local/share/static/%s" % root,
                           list(map(lambda f:root + "/" + f, files))))
    pprint(results)
    return results

webapp_content = {}

for root, dirs, files in os.walk('static'):
    for filename in files:
        filepath = os.path.join(root, filename)

        if root not in webapp_content:
            webapp_content[root] = []

        webapp_content[root].append(filepath)

pprint(webapp_content.items())

setup(name='griotte',
      version=__version__,
      description='Museum Media Player',
      long_description='',
      author=__author__,
      author_email='mblanc@erasme.org',
      url='http://griotte.erasme.org/',
      license='GPLv3',
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Environment :: Console :: Framebuffer",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: French",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: Viewers"
        ],
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
      #data_files=gen_data_files("static")
      data_files=webapp_content.items()
      # get_data_files()
                    #('/etc/init.d/', ['griotte/config/griotte.init']),
                    #('/etc/griotte.conf', ['griotte/config/griotte.conf']) ]
)

# pip install -e git://github.com/liris/websocket-client@py3#egg=websocket-client
# pip install -e git://github.com/quick2wire/quick2wire-python-api@master#egg=quick2wire-python-api
