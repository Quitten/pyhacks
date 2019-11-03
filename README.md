# pyhacks
Python module to ease writing scripts go over big amount of data in order to perform the same actions. A simple preconfigured threads and queue management and more hacking utils

Will elaborate more when it will get mature enough :)

# code example

```python
from pyhacks import Net, PyHacks

if __name__ == "__main__":
	net = Net()
	def handleItem(item):
		try:
			host = item.get("host")
			repliedToPing = net.replyToPing(host)
			ip = net.resolve(host)
			item.set("Reply To Ping", repliedToPing)
			item.set("ip", ip)
			hacks.logger.green("{} {} {}".format(host, repliedToPing, ip))
			hacks.exporter.put(item)
		except:
			pass
		return True
	
	hacks = PyHacks(handleItem, 25, "output.csv")
	hosts = hacks.parse.csv("ips.csv")
	
	for host in hosts:
		hacks.qt.put(host)
	
	hacks.finish()
    
```
