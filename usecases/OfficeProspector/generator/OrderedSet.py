from collections import OrderedDict, Set

class OrderedSet(Set):

    def __init__(self):
        self.data = OrderedDict()

    def add(self, element):
        self.data[element] = 0

    def __len__(self):
        return self.data.__len__()

    def __contains__(self, value):
        return value in self.data

    def __iter__(self):
        return self.data.__iter__()