from solution import Solution
import numpy as np


class SolutionDynamicPrograming(Solution):

    def __init__(self, knapsack_size, list_of_items):

        super().__init__(knapsack_size, list_of_items)
        self.solution_matrix = np.zeros((knapsack_size + 1, len(list_of_items)))

    def solve(self):
        for item_index in range(len(self.list_of_items)):
            self.solution_matrix[0][item_index] = 0

        for index_of_item, item in enumerate(self.list_of_items):
            self.solve_item(index_of_item, item)
            if index_of_item % 10 == 0:
                print("Item numbers: ", index_of_item, "of", len(self.list_of_items), "Solved." )

        self._add_selected_items_to_knapsack()
        self.value = self.knapsack.value
        self.weight = self.knapsack.weight

    def solve_item(self, index_of_item, item):
        for knapsack_size in range(1, self.knapsack.max_weight + 1):

            value_including_item = 0
            if item.weight <= knapsack_size:
                knapsack_size_resulting = max(0, knapsack_size - item.weight)

                value_including_item += item.value
                if index_of_item - 1 >= 0:
                    value_including_item += self.solution_matrix[knapsack_size_resulting][index_of_item - 1]

            if index_of_item - 1 >= 0:
                value_not_including_item = self.solution_matrix[knapsack_size][index_of_item - 1]
            else:
                value_not_including_item = 0

            value = max(value_not_including_item, value_including_item)

            self.solution_matrix[knapsack_size][index_of_item] = value

    def _add_selected_items_to_knapsack(self):
        knapsack_size_index = len(self.solution_matrix) - 1
        item_index = len(self.solution_matrix[0]) - 1
        while knapsack_size_index != 0 and item_index >= 0:
            has_same_value = True
            value_of_item_at_index = self.solution_matrix[knapsack_size_index][item_index]
            while has_same_value and item_index >= 0:
                if value_of_item_at_index != self.solution_matrix[knapsack_size_index][item_index - 1]:
                    has_same_value = False
                    knapsack_size_index -= self.list_of_items[item_index].weight
                    self.knapsack.add_item(self.list_of_items[item_index])
                else:
                    value_of_item_at_index = self.solution_matrix[knapsack_size_index][item_index]
                item_index -= 1

    def __str__(self):
        text = ''
        text += str(self.knapsack) + "\n"
        return text
