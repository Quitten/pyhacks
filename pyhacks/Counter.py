class Counter():
	def __init__(self, startFrom=0):
		self.counter = startFrom

	def get(self):
		return self.counter

	def plus(self,num):
		self.counter = self.counter + num
		return self.get()