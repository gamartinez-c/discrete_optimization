import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.graph = nx.Graph()

    def get_colors_of_surrounding_nodes(self, node):
        nodes_connected_to = self.get_nodes_connected_to(node)
        color_set = {*map(self.get_color_of_node, nodes_connected_to)}
        return color_set

    def get_nodes_connected_to(self, node):
        return self.graph.neighbors(node)

    def get_amount_of_connections(self, node):
        return len(self.graph.edges(node))

    def get_color_of_node(self, node):
        return self.graph.nodes[node]['color']

    def get_assignation_number(self, node):
        return self.graph.nodes[node]['assignation_number']

    def get_possible_colors_of_node(self, node):
        return self.graph.nodes[node]['possible_color']

    def does_node_has_color(self, node):
        return self.graph.nodes[node]['color'] != -1

    def set_color_of_node(self, node, color, assign_number=-1):
        self.graph.nodes[node]['color'] = color
        self.graph.nodes[node]['assignation_number'] = assign_number
        return self.propagate_constrain(node, color)

    def constrain_color(self, node, color):
        possible_colors_for_node = self.graph.nodes[node]['possible_color']
        if color in possible_colors_for_node:
            self.graph.nodes[node]['possible_color'].remove(color)

    def propagate_constrain(self, node, color):
        neighbour_nodes = self.get_nodes_connected_to(node)
        for neighbour in neighbour_nodes:
            if not self.does_node_has_color(node):
                self.constrain_color(neighbour, color)
                possible_colors_for_neighbour = self.get_possible_colors_of_node(neighbour)
                if len(possible_colors_for_neighbour) == 1:
                    self.set_color_of_node(neighbour, possible_colors_for_neighbour[0])
                    correctly_propagated = self.propagate_constrain(neighbour, color)
                    if not correctly_propagated:
                        return correctly_propagated
                if len(possible_colors_for_neighbour) == 0:
                    return False
        return True

    def get_node_with_least_possibilities(self, exclude=None):
        if exclude is None:
            exclude = set()

        nodes_to_consider = set(self.graph.nodes) - exclude
        if len(nodes_to_consider) != 0:
            selected_node = [*nodes_to_consider][0]
            min_possible_colors = self.get_possible_colors_of_node(selected_node)
            for node in nodes_to_consider:
                possible_colors = self.get_possible_colors_of_node(node)
                if possible_colors > min_possible_colors:
                    selected_node = node
                    min_possible_colors = possible_colors
            else:
                return selected_node
        return None

    def get_most_connected_node(self, exclude=None):
        if exclude is None:
            exclude = set()

        nodes_to_consider = set(self.graph.nodes) - exclude
        if len(nodes_to_consider) != 0:
            selected_node = [*nodes_to_consider][0]
            max_amount_of_connections = self.get_amount_of_connections(selected_node)
            for node in self.graph.nodes:
                amount_of_connections = self.get_amount_of_connections(node)
                if amount_of_connections > max_amount_of_connections:
                    selected_node = node
                    max_amount_of_connections = amount_of_connections
            else:
                return selected_node
        return None

    def get_cmap(self, n, name='hsv'):
        '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
        RGB color; the keyword argument name must be a standard mpl colormap name.'''
        return plt.cm.get_cmap(name, n)

    def plot(self, flag_current=False):
        colors = {
            -1: 'white',
            0: 'pink',
            1: 'red',
            2: 'blue',
            3: 'yellow',
            4: 'black',
            5: 'white',
            6: 'cyan',
            7: 'slateblue',
            8: 'darkred',
            9: 'salmon',
            10: 'gold',
            11: 'orange',
            12: 'cadetblue'
        }
        nodes_assign_number = [self.get_assignation_number(node) for node in self.graph]
        max_node_assignation = max(nodes_assign_number) if flag_current else -1

        for func_to_run in [nx.kamada_kawai_layout]:
            plt.figure(figsize=(10, 10))
            pos = func_to_run(self.graph)
            pos_2 = {key: val + [0, 0.05] for key, val in pos.items()}
            pos_3 = {key: val + [0.028, 0.05] for key, val in pos.items()}
            node = nx.draw_networkx_nodes(self.graph, pos)
            nx.draw_networkx_edges(self.graph, pos)
            nx.draw_networkx_labels(self.graph, pos, {node: self.get_color_of_node(node) for node in self.graph.nodes}, font_size=14)
            nx.draw_networkx_labels(self.graph, pos_2, {node: self.get_assignation_number(node) for node in self.graph.nodes}, font_size=9)
            nx.draw_networkx_labels(self.graph, pos_3, {node: str(node) for node in self.graph.nodes}, font_size=5)
            node.set_color(['white' if self.get_assignation_number(node) != max_node_assignation else 'red' for node in self.graph])
            node.set_color([colors[self.get_color_of_node(node)] for node in self.graph])
            node.set_edgecolor('black')

            plt.show()

    def get_return_format(self):
        return_color_list = [self.get_color_of_node(node) for node in self.graph.nodes]
        return_string = ''
        return_string += str(len(set(return_color_list))) + ' 0 \n'
        return_string += ' '.join(map(str, return_color_list))
        return return_string

