# pyhacks
Python module to ease writing scripts go over big amount of data in order to perform the same actions. A simple preconfigured threads and queue management and more hacking utils

Will elaborate more when it will get mature enough :)

# capabilities
##### PyHacks
Using all below capabilities to easily manage threads and queue to perform operations on Item objects.


```python
from pyhacks import PyHacks, Net

if __name__ == "__main__":
	net = Net()
	
	def handle_item(item):
		host = item.get("host")
		url = item.get("url")
		replied_to_ping = net.reply_to_ping(host)
		ip = net.resolve(host)
		if ip == None:
			return False
		item.set("Reply To Ping", replied_to_ping)
		item.set("ip", ip)
		hacks.logger.green("{} {} {}".format(host, replied_to_ping, ip))
		hacks.exporter.put(item)
		return True
	
	hacks = PyHacks(handle_item, 25, "output.csv")
	hosts = hacks.parse.csv("ips.csv")
	
	for host in hosts:
		hacks.qt.put(host)
	
	hacks.finish()

    
```


##### QueueThreads
QueueThreads class allows you to manage queue and threads easily.
```python
qt = QueueThreads(handle_function, num_worker_threads, logger)
qt.put({"counter":1, "key1":"value1"})
qt.finish() # waiting until job is finished
```

###### parameters
handle_function - a function recevies item parameter from queue, will be used in all threads defined, return value has to be bool
```python
def handle_item(item):
		host = item.get("host")
		url = item.get("url")
		replied_to_ping = net.reply_to_ping(host)
		ip = net.resolve(host)
		if ip == None:
			return False
		item.set("Reply To Ping", replied_to_ping)
		item.set("ip", ip)
		hacks.logger.green("{} {} {}".format(host, replied_to_ping, ip))
		hacks.exporter.put(item)
		return True

```
num_worker_threads - numbers of threads used to run handle_functions on queue items
logger - a Logger instance to be used for automatic logging

##### Parser
Parse files and returns list of Item objects
```python
parse = Parser()
items = parse.csv("ips.csv")
for item in items:
	qt.put(item)
```


##### Logger
Easy logging mechanism + writing into files under logs directory, used by QueueThreads for autoamtic logging
```python
logger = Logger(verbose=False)
logger.green("text")
logger.red("text")
logger.yellow("text")
```

##### Exporter
Exporting Item objects into a csv/txt file

```python
export = Exporter(output.csv)
export.put({"counter":1,"key1":"value"})
export.finish()
```