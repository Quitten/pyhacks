# pyhacks
Python module to ease writing scripts go over big amount of data in order to perform the same actions. A simple preconfigured threads and queue management and more hacking utils

Will elaborate more when it will get mature enough :)

# code example

```python
from pyhacks import Logger, QueueThreads, Exporter, Parser, Net

if __name__ == "__main__":
	def handleItem(item):
		try:
			host = item.get("host")
			item.set("Reply To Ping", net.replyToPing(host))
			item.set("ip", net.resolve(host))
			export.put(item)
		except:
			pass
		return True
	
	net = Net()
	logger = Logger()
	parse = Parser()
	export = Exporter("output.csv")
	
	numbersOfThreads = 1
	x = QueueThreads(handleItem, numbersOfThreads, logger, True)
	
	hosts = parse.csv("ips.csv")
	for host in hosts:
		x.put(host)
		
	x.finish()
	export.finish()
    
```
