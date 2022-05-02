from node import Node
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


class Tree:
    def __init__(self, list_of_items, capacidad):
        self.list_of_items = list_of_items
        self.capacidad = capacidad
        self.mejor_nodo = None
        self.node_inicial = None
        self.edge_node_list = []

    def run(self):
        self.node_inicial = Node(self.list_of_items, self.capacidad, 0, self, False)
        self.edge_node_list.append(self.node_inicial)
        self.node_inicial.run()

    def plot_current_tree(self):
        graph = nx.Graph()
        graph.add_node(self.node_inicial.index_creation)
        self.node_inicial.add_information_to_graph(graph)

        color_map = []
        for node in graph:
            decision = 0
            if node != self.node_inicial.index_creation:
                decision = self.node_inicial.get_decision_of_node(node)
            if decision == 0:
                color_map.append('red')
            else:
                color_map.append('green')

        pos = graphviz_layout(graph, prog="dot")
        nx.draw(graph, pos, node_color=color_map, with_labels=True)
        plt.show()

    def get_best_solution_items(self):
        return self.node_inicial.get_solution_path(self.mejor_nodo)
