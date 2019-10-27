import os
import uuid
import queue
import threading
from Item import Item
from Counter import Counter
from constants import *

def cleanup():
	try:
		os.remove(LOG_FILE_NAME)
		os.remove(SUCESS_FILE_NAME)
	except:
		pass

class QueueThreads():
	def __init__(self, handleFunction, num_worker_threads, logger,cleanup = False):
		self.q = queue.Queue()
		self.counter = Counter()
		self.threads = []
		self.uniqSuccess = []
		self.logger = logger
		self.num_worker_threads = num_worker_threads
		self.init(handleFunction)

	def init(self, handleFunction):
		if cleanup:
		    cleanup()
		if os.path.exists(SUCESS_FILE_NAME):
			self.uniqSuccess = os.popen('sort {} | uniq'.format(SUCESS_FILE_NAME)).read()
			with open(SUCESS_FILE_NAME, "w") as myfile:
				myfile.write(self.uniqSuccess)

		def worker():
			while True:
				item = self.q.get()
				if item is None:
					self.q.task_done()
					break
				item.verifyKey("counter")
				if self.uniqSuccess != []:
					if self.isItemHanlded(item):
						self.logger.debug("Skipping item #{}, already handeled".format(item.get("counter")))
						self.q.task_done()
						continue

				self.logger.debug("Handling item #{}".format(item.get("counter")))
				if handleFunction(item):
					self.logger.success(item)
				self.q.task_done()

		for i in range(self.num_worker_threads):
			t = threading.Thread(target=worker)
			t.start()
			self.threads.append(t)
			self.logger.debug("Initializing thread #{}".format(len(self.threads)))
		self.logger.debug("ID: {}".format(uuid.uuid4()))

	def isItemHanlded(self, item):
		return str(item.get("counter")) in self.uniqSuccess

	def put(self, item):
		itemObject = Item(item)
		if not itemObject.hasKey("counter"):
			itemObject.set("counter", self.counter.plus(1))
		self.q.put(itemObject)

	def finish(self):
		for i in range(self.num_worker_threads):
			self.q.put(None)
		for t in self.threads:
		    t.join()
		self.q.join()
		self.logger.finish()
		