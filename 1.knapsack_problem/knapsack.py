class Knapsack:
    def __init__(self, max_weight):
        self.max_weight = max_weight
        self.items = []
        self.weight = 0
        self.value = 0

    def add_item(self, item):
        if (self.weight + item.weight) <= self.max_weight:
            self.items.append(item)
            self.value += item.value
            self.weight += item.weight
            return True
        return False

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            self.value -= item.value
            self.weight -= item.weight
            return True
        return False

    def fill_knapsack_from_list(self, list_of_items):
        for item in list_of_items:
            self.add_item(item)

    def __str__(self):
        return f'Value: {self.value} | Weight: {self.weight} | Number of Items {len(self.items)}'
