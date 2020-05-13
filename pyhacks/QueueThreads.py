import os
import uuid
import queue
import threading
from .Item import Item
from .Logger import Logger
from .Counter import Counter
from .constants import *

def cleanup():
	try:
		for path in ALL_PATHS:
			os.remove(path)
	except:
		pass

class QueueThreads:
	def __init__(self, handle_function, num_worker_threads, logger, cleanup = False):
		self.logger = logger
		self.threads = []
		self.success_list = []
		self.q = queue.Queue()
		self.counter = Counter()
		self.cleanup = cleanup
		self.num_worker_threads = num_worker_threads
		self.init(handle_function)

	def init(self, handle_function):
		if self.cleanup:
		    cleanup()

		if os.path.exists("{}/{}".format(os.getcwd(), SUCESS_FILE_NAME)):
			self.success_list = os.popen('sort {} | uniq'.format(SUCESS_FILE_NAME)).read()
			with open(SUCESS_FILE_NAME, "w") as myfile:
				myfile.write(self.success_list)

		def worker():
			while True:
				item = self.q.get()
				if item is None:
					self.q.task_done()
					break
				item.verify_key("counter")
				if self.success_list != []:
					if self.is_item_handled(item):
						self.logger.debug("Skipping item #{}, already handeled".format(item.get("counter")))
						self.q.task_done()
						continue

				self.logger.debug("Handling item #{}".format(item.get("counter")))
				try:
					handle_function_result = handle_function(item)
				except Exception as err:
					self.logger.red("Error in handle function: {}".format(err))
					self.logger.exception({"exception": err, "item": item})
					self.logger.fail(item)
					self.q.task_done()
					continue
				if type(handle_function_result) != bool:
					# TODO: use self.logger.finish() to wait error logs will be written
					self.logger.red("Error: handle function return value is not boolean")
					self.logger.fail(item)
					self.q.task_done()
					os._exit(1)
					
				elif handle_function_result:
					self.logger.success(item)
				else:
					self.logger.fail(item)
				self.q.task_done()

		for i in range(self.num_worker_threads):
			t = threading.Thread(target=worker)
			t.start()
			self.threads.append(t)
			self.logger.debug("Initializing thread #{}".format(len(self.threads)))
		self.logger.debug("ID: {}".format(uuid.uuid4()))

	def is_item_handled(self, item):
		return str(item.get("counter")) in self.success_list

	def put(self, item):
		self.q.put(item)

	def finish(self):
		for i in range(self.num_worker_threads):
			self.q.put(None)
		for t in self.threads:
		    t.join()
		self.q.join()
		self.logger.finish()
		