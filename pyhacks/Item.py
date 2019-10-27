class Item():
    # add default counter
    def __init__(self, item):
        self.item = item

    def hasKey(self, keyName):
        return keyName in self.item

    def verifyKey(self, keyName):
        if type(keyName)!=str:
            raise Exception("Key type excpected to be str but got {}".format(type(keyName)))
        if self.hasKey(keyName):
            return True
        else:
            raise Exception("Key {} doesn't exist in item: {}".format(keyName, self.item))

    def verifyKeys(self, keys):
        if type(keys)!=list:
            raise Exception("Keys type excpected to be list but got {}".format(type(keys)))
        for key in keys:
            self.verifyKey(self.item, key)
        return True

    def get(self, keyName):
        self.verifyKey(keyName)
        return self.item[keyName]
    
    def set(self, keyName, value):
        self.item[keyName] = value

        