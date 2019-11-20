class Item:
    def __init__(self, item, counter):
        if type(item) == str:
            self.item = {"counter": counter, "content": item}
        elif type(item) == dict:
            item["counter"] = counter
            self.item = item
        else:
            raise Exception("item is not str or dict")
    
    def __str__(self):
        return str(self.item)

    def has_key(self, key_name):
        return key_name in self.item

    def get(self, key_name):
        return self.item.get(key_name)
    
    def keys(self):
        return self.item.keys()
    
    def set(self, key_name, value):
        self.item[key_name] = value

        