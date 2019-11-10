class Item:
    # add default counter
    def __init__(self, item, counter):
        if type(item) == str:
            self.item = {"counter": counter, "content": item}
        elif type(item) == dict:
            item["counter"] = counter
            self.item = item
        else:
            raise Exception("item is not str or dict")

    def has_key(self, key_name):
        return key_name in self.item

    def verify_key(self, key_name):
        if type(key_name)!=str:
            raise Exception("Key type excpected to be str but got {}".format(type(key_name)))
        if self.has_key(key_name):
            return True
        else:
            raise Exception("Key {} doesn't exist in item: {}".format(key_name, self.item))

    def verify_keys(self, keys):
        if type(keys)!=list:
            raise Exception("Keys type excpected to be list but got {}".format(type(keys)))
        for key in keys:
            self.verify_key(self.item, key)
        return True

    def get(self, key_name):
        self.verify_key(key_name)
        return self.item[key_name]
    
    def keys(self):
        return self.item.keys()
    
    def set(self, key_name, value):
        self.item[key_name] = value

        