import os
import uuid
import queue
import threading

LOG_FILE_NAME = "log.txt"
SUCESS_FILE_NAME = "success.txt"

def getCSV(fileName, delimiter, quotechar):
    csvfile = open(fileName, 'r')
    spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
    currentLine = 0
    csvContent = []

    keys = []
    for row in spamreader:
        currentLine = currentLine + 1
        if currentLine == 1:
            keys = row
            continue
        obj = {}

        if len(keys) != len(row):
        	raise Exception("Malformed CSV file key length != row length")
        for i in range(len(keys)):
            obj[keys[i]] = row[i]
        csvContent.append(obj)
    return csvContent

def verifyKey(item, keyName):
	if type(keyName)!=str:
		raise Exception("Key type excpected to be str but got {}".format(type(keyName)))
	if keyName in item:
		return True
	else:
		raise Exception("Key {} doesn't exist in item".format(keyName))

def verifyKeys(item, keys):
	if type(keys)!=list:
		raise Exception("Keys type excpected to be list but got {}".format(type(keyName)))
	for key in keys:
		verifyKey(item,key)
	return True


class Logger():
	def __init__(self, verbose = True):
		self.q = queue.Queue()
		self.thread = None
		self.verbose = verbose
		self.init()

	def init(self):
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
		t.start()
		self.thread = t

	def _write(self, fileName,content):
		with open(fileName, "a") as myfile:
			myfile.write("{}\n".format(content))

	def log(self, content, verbose = True):
		if self.verbose and verbose:
			print(content)
		self.q.put({"fileName":LOG_FILE_NAME, "content":content})

	def success(self, item):
		verifyKey(item,"counter")
		self.q.put({"fileName":SUCESS_FILE_NAME, "content":item["counter"]})

	def finish(self):
		self.q.put(None)
		self.thread.join()
		self.q.join()

class QueueThreads():
	def __init__(self, handleFunction, num_worker_threads, logger = Logger()):
		self.q = queue.Queue()
		self.threads = []
		self.uniqSuccess = []
		self.logger = logger
		self.num_worker_threads = num_worker_threads
		self.init(handleFunction)

	def init(self, handleFunction):
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
				verifyKey(item,"counter")
				if self.uniqSuccess != []:
					if self.isItemHanlded(item):
						self.logger.log("Skipping item #{}, already handeled".format(item["counter"]))
						self.q.task_done()
						continue

				self.logger.log("Handling item #{}".format(item["counter"]))
				if handleFunction(item):
					self.logger.success(item)
				self.q.task_done()

		for i in range(self.num_worker_threads):
			t = threading.Thread(target=worker)
			t.start()
			self.threads.append(t)
			self.logger.log("Initializing thread #{}".format(len(self.threads)))
		self.logger.log("ID: {}".format(uuid.uuid4()))

	def isItemHanlded(self, item):
		return str(item["counter"]) in self.uniqSuccess

	def put(self, item):
		self.q.put(item)

	def finish(self):
		for i in range(self.num_worker_threads):
			self.q.put(None)
		for t in self.threads:
		    t.join()
		self.q.join()
		self.logger.finish()

class Counter():
	def __init__(self, startFrom=0):
		self.counter = startFrom

	def get(self):
		return self.counter

	def plus(self,num):
		self.counter = self.counter + num
		return self.get()

# user code example:

# should return bool
def handleItem(item):
	return True

c = Counter()
x = QueueThreads(handleItem, 25)
for i in range(10):
	x.put({"counter":c.plus(1)})
x.finish()
