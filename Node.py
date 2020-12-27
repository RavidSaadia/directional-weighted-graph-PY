class Node  :
    _id = 0
    def __init__(self, inside : {}, outside : {}, info : ""):
        self._id += 1
        self.inside = inside
        self.outside = outside
        self.info = info

    def connect(self,  node):
        self.outside[node.get_id()] = node
        node.inside[self.get_id()] = self

    def get_id(self):
        return self._id

    def get_info(self):
        return self.info

