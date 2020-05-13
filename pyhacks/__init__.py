# -*- coding: utf-8 -*-

"""
Pyhacks library
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2019 by Barak Tawily.
"""

__title__ = 'pyhacks'
__version__ = '1.0.20'
__build__ = 0x010020
__author__ = 'Barak Tawily'
__license__ = 'MIT'
__copyright__ = 'Copyright 2019 Barak Tawily'

from .QueueThreads import QueueThreads
from .Exporter import Exporter
from .Parser import Parser
from .Logger import Logger
from .Net import Net
# TOOD: Add headless chrome module

class PyHacks:
    def __init__(self, handle_function, num_worker_threads, export_file_name, cleanup = False, verbose = False):
        self.parse = Parser()
        self.logger = Logger(verbose)
        self.exporter = Exporter(export_file_name)
        self.num_worker_threads = num_worker_threads
        self.export_file_name = export_file_name
        self.qt = QueueThreads(handle_function, num_worker_threads, self.logger, cleanup)
    
    def handle(self, item):
        self.qt.put(item)
    
    def add_to_queue(self, item, key_name=""):
        if type(item) == str and key_name != "":
            self.qt.put({key_name: item})
        else:
            self.qt.put(item)

    def export(self, item):
        self.exporter.put(item)

    def finish(self):
        self.qt.finish()
        self.exporter.finish()
