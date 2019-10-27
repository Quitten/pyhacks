import os
import csv
import uuid
import queue
import threading
from QueueThreads import QueueThreads
from Parser import Parser
from Logger import Logger

# TODO:
# advanced objects keys validators
# helper functions for checking stuff

# BUG: while supplying my own logger
# logger = Logger()
# x = QueueThreads(handleItem, 25, logger)
# logger.finish()