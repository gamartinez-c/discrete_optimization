from solution import Solution


class SolutionGreedy(Solution):
    possible_solving_method = ['value', 'weight', 'value-weight', 'weight-value',
                               'density', 'density-weight', 'density-value' ]

    def __init__(self, knapsack_size, list_of_items, solving_method):

        super().__init__(knapsack_size, list_of_items)
        self.method = solving_method

    def solve(self):
        if self.method in SolutionGreedy.possible_solving_method:
            self.solve_method(self.method)
            self.value = self.knapsack.value
            self.weight = self.knapsack.weight
        else:
            print('The method is not identify into one of the possible method.')

    def solve_method(self, method):
        order_item_list = self.get_items_list_ordered(method)
        self.knapsack.fill_knapsack_from_list(order_item_list)

    def get_items_list_ordered(self, method):
        ordered_list = []
        original_list = self.list_of_items.copy()
        for _ in range(len(self.list_of_items)):
            item_to_add = original_list[0]
            for item in original_list:
                if method == 'value':
                    if item.value >= item_to_add.value:
                        item_to_add = item
                elif method == 'weight':
                    if item.weight <= item_to_add.weight:
                        item_to_add = item
                elif method == 'value-weight':
                    if item.value >= item_to_add.value:
                        if item.weight <= item_to_add.weight:
                            item_to_add = item
                elif method == 'weight-value':
                    if item.weight <= item_to_add.weight:
                        if item.value >= item_to_add.value:
                            item_to_add = item
                elif method == 'density':
                    if item.get_density() >= item_to_add.get_density():
                        item_to_add = item
                elif method == 'density-weight':
                    if item.get_density() >= item_to_add.get_density():
                        if item.weight <= item_to_add.weight:
                            item_to_add = item
                elif method == 'density-value':
                    if item.get_density() >= item_to_add.get_density():
                        if item.value >= item_to_add.value:
                            item_to_add = item
                else:
                    item_to_add = item
            else:
                ordered_list.append(item_to_add)
                original_list.remove(item_to_add)

        return ordered_list

    def __str__(self):
        text = ''
        text += self.method + " || " + str(self.knapsack)
        return text
