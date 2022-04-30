from knapsack import Knapsack


class Solution:
    def __init__(self, knapsack_size, list_of_items):
        self.knapsack = Knapsack(knapsack_size)
        self.list_of_items = list_of_items
        self.value = None
        self.weight = None

    def get_output_format(self):
        output_text = '' + str(self.value) + ' 0\n'

        list_boolean = [0 for _ in range(len(self.list_of_items))]
        for item in self.knapsack.items:
            list_boolean[item.index] = 1
        output_text += " ".join(map(str, list_boolean))

        return output_text
