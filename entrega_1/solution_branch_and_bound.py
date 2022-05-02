from solution import Solution
from tree import Tree


class SolutionBranchAndBound(Solution):

    def __init__(self, knapsack_size, list_of_items):

        super().__init__(knapsack_size, list_of_items)
        self.tree = None

    def solve(self):
        self.list_of_items.sort(key=lambda x: x.get_density())

        self.tree = Tree(self.list_of_items, self.knapsack.max_weight)
        self.tree.run()

        # self.tree.plot_current_tree()

        self._add_selected_items_to_knapsack()
        self.value = self.knapsack.value
        self.weight = self.knapsack.weight

    def _add_selected_items_to_knapsack(self):
        list_of_selected_items = self.tree.get_best_solution_items()
        for item in list_of_selected_items:
            self.knapsack.add_item(item)

    def __str__(self):
        text = ''
        text += str(self.knapsack) + "\n"
        return text
