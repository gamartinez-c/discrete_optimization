import sys
sys.setrecursionlimit(30000)


class Node:
    counter = 0

    def __init__(self, list_of_items, capacidad, valor, tree, adding_node):
        self.list_of_items = list_of_items.copy()
        self.capacidad = capacidad
        self.valor = valor
        self.tree = tree
        self.nodo_1 = None
        self.nodo_0 = None
        self.index_creation = Node.counter
        self.adding_node = adding_node
        Node.counter += 1

    def get_relaxed_value(self):
        potential_value = 0
        current_capacity = self.capacidad
        list_of_items = self.list_of_items.copy()
        can_i_add_portion_of_item = current_capacity > 0 and len(list_of_items) != 0
        while can_i_add_portion_of_item:
            fraction_to_add = 1 if list_of_items[0].weight < current_capacity else current_capacity/list_of_items[0].weight
            potential_value += list_of_items[0].value * fraction_to_add
            current_capacity -= list_of_items[0].weight * fraction_to_add

            list_of_items = list_of_items[1:]
            can_i_add_portion_of_item = current_capacity > 0 and len(list_of_items) != 0

        return potential_value + self.valor

    def run(self):
        item_over_decision = self.list_of_items[0]

        if self in self.tree.edge_node_list:
            self.tree.edge_node_list.remove(self)

        self.nodo_0 = Node(self.list_of_items[1:], self.capacidad, self.valor, self.tree, False)
        self.tree.edge_node_list.append(self.nodo_0)
        if item_over_decision.weight < self.capacidad:
            self.nodo_1 = Node(self.list_of_items[1:], self.capacidad - item_over_decision.weight, self.valor + item_over_decision.value, self.tree, True)
            self.tree.edge_node_list.append(self.nodo_1)

        best_node = self.tree.edge_node_list[0]
        for edge_node in self.tree.edge_node_list:
            if edge_node.get_relaxed_value() > best_node.get_relaxed_value():
                best_node = edge_node

        if len(best_node.list_of_items) != 0:
            best_node.run()
        else:
            self.tree.mejor_nodo = best_node
            print('Finish.')

    def get_solution_path(self, nodo):

        if self == nodo:
            return [self]
        else:
            return_0 = None if self.nodo_0 is None else self.nodo_0.get_solution_path(nodo)
            return_1 = None if self.nodo_1 is None else self.nodo_1.get_solution_path(nodo)

            if return_0 is not None:
                return return_0.append(self)
            elif return_1 is not None:
                return return_1.append(self)
            else:
                return None

    def get_decision_of_node(self, node_index):

        if self.nodo_0 is not None:
            if self.nodo_0.index_creation == node_index:
                return 0
        elif self.nodo_1 is not None:
            if self.nodo_1.index_creation == node_index:
                return 1

        return_0 = None if self.nodo_0 is None else self.nodo_0.get_decision_of_node(node_index)
        return_1 = None if self.nodo_1 is None else self.nodo_1.get_decision_of_node(node_index)
        if return_0 is not None:
            return return_0
        else:
            return return_1

    def add_information_to_graph(self, graph):
        if self.nodo_0 is not None:
            graph.add_node(self.nodo_0.index_creation)
            graph.add_edge(self.index_creation, self.nodo_0.index_creation)
            self.nodo_0.add_information_to_graph(graph)

        if self.nodo_1 is not None:
            graph.add_node(self.nodo_1.index_creation)
            graph.add_edge(self.index_creation, self.nodo_1.index_creation)
            self.nodo_1.add_information_to_graph(graph)

    def debugging_print(self):
        print('node calculation no: c:', self.nodo_0.capacidad,
              'v:', self.nodo_0.valor,
              '\tMejor', self.tree.mejor_nodo,
              '\tEstimado:', self.nodo_0.estimacion,
              '\tLista_valores', [item.value for item in self.nodo_0.list_of_items])

    """def relaxed_best(self):
            list_of_items = self.list_of_items[1:]
            k = self.capacidad
            value = 0
            for i in range(len(list_of_items)):
                if list_of_items[i].weight < k:
                    k -= list_of_items[i].weight
                    value += list_of_items[i].value
                else:
                    fraction = k / list_of_items[i].weight
                    value += fraction * list_of_items[i].value

            return value"""
