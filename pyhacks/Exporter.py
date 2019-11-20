import os
import csv
import queue
import threading

class Exporter:
	def __init__(self, file_name, delimiter=' '):
		self.q = queue.Queue()
		self.file_name = file_name
		self.delimiter = delimiter
		self.thread = self.init_thread()
		if (os.path.exists(self.file_name)):
			userInput = input('Export file exists, overwrite file? [Y/n]:\n')
			if userInput.lower() == 'y' or userInput == '':
				os.remove(self.file_name)
		self.file_format = os.path.splitext(file_name)[1]

	def init_thread(self):
		def worker():
			while True:
				item = self.q.get()
				if item is None:
					self.q.task_done()
					break

				if self.file_format == '.txt':
					self.write_txt(item)
				elif self.file_format == '.csv':
					self.write_csv(item)

				self.q.task_done()
		t = threading.Thread(target=worker)
		t.start()
		return t
    
	def write_txt(self, item):
		content = ''
		content = "{}{} ".format(content, item.get('counter'))
		for key in item.keys():
			if key == 'counter':
				continue
			content = "{}{}{}".format(content, item.get(key), self.delimiter)

		with open(self.file_name, "a") as myfile:
			myfile.write("{}\n".format(content))

	def write_csv(self, item):
		with open(self.file_name, mode='a') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			if csv_file.tell() == 0:
				# TODO: add quotes to keys
				csv_writer.writerow(item.keys())
			data = []
			for key in item.keys():
				data.append(item.get(key))
			csv_writer.writerow(data)

	def put(self, item):
		self.q.put(item)

	def finish(self):
		self.q.put(None)
		self.thread.join()
		self.q.join()
