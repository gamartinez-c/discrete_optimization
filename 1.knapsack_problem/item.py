class Item:
    def __init__(self, value, weight, index):
        self.value = value
        self.weight = weight
        self.index = index

    def get_density(self):
        return self.value/self.weight

    def __str__(self):
        return f'Index: {self.index} | Value: {self.value} | Weight: {self.weight}'