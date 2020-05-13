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

    def verify_key(self, key_name):
        if type(key_name)!=str:
            raise Exception("Key type excpected to be str but got {}".format(type(key_name)))
        if key_name in self.item:
            return True
        else:
            raise Exception("Key {} doesn't exist in item: {}".format(key_name, self.item))

    def verify_keys(self, keys):
        if type(keys)!=list:
            raise Exception("Keys type excpected to be list but got {}".format(type(keys)))
        for key in keys:
            self.verify_key(key)
        return True
        
    def has_key(self, key_name):
        return key_name in self.item

    def get(self, key_name):
        return self.item.get(key_name)
    
    def keys(self):
        return self.item.keys()
    
    def set(self, key_name, value):
        self.item[key_name] = value

        