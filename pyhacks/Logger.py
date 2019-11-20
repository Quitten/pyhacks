import os
import queue
import threading
from .constants import *

def verify_key(item, key_name):
	if type(key_name)!=str:
		raise Exception("Key type excpected to be str but got {}".format(type(key_name)))
	if key_name in item:
		return True
	else:
		raise Exception("Key {} doesn't exist in item: {}".format(key_name, item))

def verify_keys(item, keys):
	if type(keys)!=list:
		raise Exception("Keys type excpected to be list but got {}".format(type(keys)))
	for key in keys:
		verify_key(item, key)
	return True

class Logger:
	def __init__(self, verbose = False):
		self.q = queue.Queue()
		self.thread = self.init_thread()
		self.verbose = verbose

	def init_thread(self):
		logs_dir_path = "{}/logs/".format(os.getcwd())
		if not os.path.exists(logs_dir_path):
			os.mkdir(logs_dir_path)
		def worker():
			while True:
				log_object = self.q.get()
				if log_object is None:
					self.q.task_done()
					break
				verify_keys(log_object,["file_name", "content"])
				self._write(log_object["file_name"], log_object["content"])
				if (log_object["file_name"] != LOG_FILE_NAME):
					self._write(LOG_FILE_NAME, log_object["content"])
				self.q.task_done()
		t = threading.Thread(target=worker)
		t.start()
		return t

	def _write(self, file_name, content):
		try:
			with open(file_name, "a") as myfile:
				myfile.write("{}\n".format(content))
		except Exception as err:
			self.red("Writing error: {}".format(err))
			os._exit(1)

	def green(self, content, file_name = LOG_FILE_NAME, verbose = True):
		if verbose:
			print('\033[32m', content, '\033[0m', sep='')
		self.q.put({"file_name":file_name, "content":content})

	def red(self, content, file_name = LOG_FILE_NAME, verbose = True):
		if verbose:
		    print('\033[31m', content, '\033[0m', sep='')

		self.q.put({"file_name":file_name, "content":content})

	def yellow(self, content, file_name = LOG_FILE_NAME, verbose = True):
		if verbose:
			    print('\033[33m', content, '\033[0m', sep='')
		self.q.put({"file_name":file_name, "content":content})

	def log(self, content, file_name = LOG_FILE_NAME, verbose = True):
		if verbose:
			print(content)
		self.q.put({"file_name":file_name, "content":content})
	
	def debug(self,content):
		self.log(content,verbose=self.verbose)

	def success(self, item):
		item.verify_key("counter")
		self.q.put({"file_name":SUCESS_FILE_NAME, "content":item.get("counter")})

	def fail(self, item):
		item.verify_key("counter")
		self.q.put({"file_name":FAIL_FILE_NAME, "content":item.get("counter")})

	def exception(self, obj):
		obj.get("item").verify_key("counter")
		self.q.put({"file_name":EXCEPTION_FILE_NAME, "content":obj})

	def put(self, item):
		self.q.put(item)

	def finish(self):
		self.q.put(None)
		self.thread.join()
		self.q.join()