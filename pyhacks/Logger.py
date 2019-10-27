import queue
import threading
from .constants import *

def verifyKey(item, keyName):
	if type(keyName)!=str:
		raise Exception("Key type excpected to be str but got {}".format(type(keyName)))
	if keyName in item:
		return True
	else:
		raise Exception("Key {} doesn't exist in item: {}".format(keyName, item))

def verifyKeys(item, keys):
	if type(keys)!=list:
		raise Exception("Keys type excpected to be list but got {}".format(type(keys)))
	for key in keys:
		verifyKey(item, key)
	return True

class Logger():
	def __init__(self, verbose = False):
		self.q = queue.Queue()
		self.thread = self.initThread()
		self.thread.start()
		self.verbose = verbose

	def initThread(self):
		def worker():
			while True:
				logObj = self.q.get()
				if logObj is None:
					self.q.task_done()
					break
				verifyKeys(logObj,["fileName","content"])
				self._write(logObj["fileName"],logObj["content"])
				self.q.task_done()
		t = threading.Thread(target=worker)
		return t

	def _write(self, fileName,content):
		with open(fileName, "a") as myfile:
			myfile.write("{}\n".format(content))

	def log(self, content, verbose = True):
		if verbose:
			print(content)
		self.q.put({"fileName":LOG_FILE_NAME, "content":content})
	
	def debug(self,content):
		self.log(content,self.verbose)

	def success(self, item):
		item.verifyKey("counter")
		self.q.put({"fileName":SUCESS_FILE_NAME, "content":item.get("counter")})

	def put(self, item):
		self.q.put(item)

	def finish(self):
		self.q.put(None)
		self.thread.join()
		self.q.join()