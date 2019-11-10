# pyhacks
Python module to ease writing scripts go over big amount of data in order to perform the same actions. A simple preconfigured threads and queue management and more hacking utils

Will elaborate more when it will get mature enough :)

# code example

```python
from pyhacks import PyHacks, Net

if __name__ == "__main__":
	net = Net()

	def handle_item(item):
		host = item.get("host")
		url = item.get("url")
		replied_to_ping = net.reply_to_ping(host)
		ip = net.resolve(host)
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
