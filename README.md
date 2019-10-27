# pyhacks
Python module to ease writing scripts go over big amount of data in order to perform the same actions. A simple preconfigured threads and queue management and more hacking utils

Will elaborate more when it will get mature enough :)

# code example

```python
from pyhacks import Logger, QueueThreads, Parser

if __name__ == "__main__":
	def handleItem(item):
        	content = "{},{}".format(item.get("Name"),item.get("Phone 1 - Value"))
        	logger.log(content, "output.txt")
		return True

	logger = Logger()
	parse = Parser()
	x = QueueThreads(handleItem, 25, logger, True)

	contacts = parse.csv("contacts.csv")

	for contact in contacts:
		x.put(contact)
		
	x.finish()
    
```
