class User:
    def __init__(self, uuid, name):
      self.name = name
      self._uuid = uuid
    
    def get_name(self):
        return self.name
        