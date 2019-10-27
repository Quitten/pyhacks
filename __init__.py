# -*- coding: utf-8 -*-

#   __
#  /__)  _  _     _   _ _/   _
# / (   (- (/ (/ (- _)  /  _)
#          /

"""
Pyhacks library
~~~~~~~~~~~~~~~~~~~~~

Requests is an HTTP library, written in Python, for human beings. Basic GET
usage:

   >>> import requests
   >>> r = requests.get('https://www.python.org')
   >>> r.status_code
   200
   >>> 'Python is a programming language' in r.content
   True

... or POST:

   >>> payload = dict(key1='value1', key2='value2')
   >>> r = requests.post('http://httpbin.org/post', data=payload)
   >>> print(r.text)
   {
     ...
     "form": {
       "key2": "value2",
       "key1": "value1"
     },
     ...
   }

:copyright: (c) 2019 by Barak Tawily.
"""

__title__ = 'pyhacks'
__version__ = '1.0.0'
__build__ = 0x01000
__author__ = 'Barak Tawily'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2019 Barak Tawily'

from pyhacks import *
