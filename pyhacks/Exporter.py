import os
import csv
import queue
import threading

class Exporter:
	def __init__(self, fileName, delimiter=' '):
		self.q = queue.Queue()
		self.fileName = fileName
		self.delimiter = delimiter
		self.thread = self.initThread()
		if (os.path.exists(self.fileName)):
			userInput = input('Export file exists, overwrite file? [y/n]:\n')
			if userInput == 'y':
				os.remove(self.fileName)
		self.fileFormat = os.path.splitext(fileName)[1]

	def initThread(self):
		def worker():
			while True:
				item = self.q.get()				
				if item is None:
					self.q.task_done()
					break

				if self.fileFormat == '.txt':
					self.writeTXT(item)
				elif self.fileFormat == '.csv':
					self.writeCSV(item)

				self.q.task_done()
		t = threading.Thread(target=worker)
		t.start()
		return t
    
	def writeTXT(self, item):
		content = ''
		content = "{}{} ".format(content, item.get('counter'))
		for key in item.keys():
			if key == 'counter':
				continue
			content = "{}{}{}".format(content, item.get(key), self.delimiter)

		with open(self.fileName, "a") as myfile:
			myfile.write("{}\n".format(content))

	def writeCSV(self, item):
		with open(self.fileName, mode='a') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			if item.get('counter') == 1:
				csv_writer.writerow(item.keys())
			data = [item.get('counter')]
			for key in item.keys():
				if key == 'counter':
					continue
				data.append(item.get(key))
			csv_writer.writerow(data)

	def put(self, item):
		self.q.put(item)

	def finish(self):
		self.q.put(None)
		self.thread.join()
		self.q.join()
