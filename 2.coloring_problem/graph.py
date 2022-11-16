import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.nodes_dict = dict()
        self.nodes_with_color_assign = []

    def add_node(self, node):
        self.nodes_dict[node.id] = node

    def get_node_by_id(self, node_id):
        return self.nodes_dict[node_id]

    def reset_nodes_list(self, nodes_id_list):
        nodes_to_reset = []

        # Reset color
        for node_id in nodes_id_list:
            node = self.get_node_by_id(node_id)
            nodes_to_reset.append(node)
            node.color = -1
            node.possible_colors = node.original_possible_colors.copy()
            self.nodes_with_color_assign.remove(node)

        # Reset constraints
        for node in nodes_to_reset:
            colors_surrounding = node.get_colors_of_surrounding_nodes()
            for color in colors_surrounding:
                node.constrain_color(color)

    def add_edge(self, id_node_1, id_node_2):
        node_1 = self.get_node_by_id(id_node_1)
        node_2 = self.get_node_by_id(id_node_2)

        node_1.nodes_connected_to.append(node_2)
        node_2.nodes_connected_to.append(node_1)

    def set_color_of_node(self, node_id, color):
        node = self.get_node_by_id(node_id)
        node.color = color
        self.nodes_with_color_assign.append(node)
        return self.propagate_constrain(node, color)

    def propagate_constrain(self, node, color):
        for neighbour in node.nodes_connected_to:
            if neighbour.id == 18:
                print('', end='')
            neighbour.constrain_color(color)

        for neighbour in node.nodes_connected_to:
            if not neighbour.does_node_has_color():
                possible_colors_for_neighbour = neighbour.possible_colors
                if len(possible_colors_for_neighbour) == 1:
                    correctly_propagated = self.set_color_of_node(neighbour.id, possible_colors_for_neighbour[0])
                    if not correctly_propagated:
                        return False
                if len(possible_colors_for_neighbour) == 0:
                    return False
        return True

    def get_node_with_least_possibilities(self, exclude=None):
        if exclude is None:
            exclude = set()

        nodes_to_consider = set(self.nodes_dict.values()) - exclude
        if len(nodes_to_consider) != 0:
            selected_node = [*nodes_to_consider][0]
            min_possible_colors = selected_node.possible_colors
            for node in nodes_to_consider:
                possible_colors = node.possible_colors
                if possible_colors > min_possible_colors:
                    selected_node = node
                    min_possible_colors = possible_colors
            else:
                return selected_node
        return None

    def get_most_connected_node(self, exclude=None):
        if exclude is None:
            exclude = set()

        nodes_to_consider = set(self.nodes_dict.values()) - exclude
        if len(nodes_to_consider) != 0:
            selected_node = [*nodes_to_consider][0]
            max_amount_of_connections = selected_node.get_amount_of_connections()
            for node in nodes_to_consider:
                amount_of_connections = node.get_amount_of_connections()
                if amount_of_connections > max_amount_of_connections:
                    selected_node = node
                    max_amount_of_connections = amount_of_connections
            else:
                return selected_node
        return None

    def get_node_under_criteria(self, criteria, exclude_nodes):
        if criteria == 'most_connected':
            node = self.get_most_connected_node(exclude_nodes)
        else:
            node = self.get_node_with_least_possibilities(exclude_nodes)
        return node

    def plot(self):
        colors = {-1: 'white', 0: 'pink', 1: 'red', 2: 'blue', 3: 'yellow', 4: 'black', 5: 'cadetblue',
                  6: 'cyan', 7: 'slateblue', 8: 'darkred', 9: 'salmon', 10: 'gold', 11: 'orange'}

        nx_graph = nx.Graph()
        for node_id, node in self.nodes_dict.items():
            nx_graph.add_node(node_id, color=node.id)
        edges = [(node_1.id, node_2.id) for node_1 in self.nodes_dict.values() for node_2 in node_1.nodes_connected_to]
        nx_graph.add_edges_from(edges)

        for func_to_run in [nx.kamada_kawai_layout]:
            plt.figure(figsize=(10, 10))
            pos = func_to_run(nx_graph)
            pos_3 = {key: val + [0.028, 0.05] for key, val in pos.items()}
            node = nx.draw_networkx_nodes(nx_graph, pos)
            nx.draw_networkx_edges(nx_graph, pos)
            nx.draw_networkx_labels(nx_graph, pos, {node.id: node.color for node in self.nodes_dict.values()}, font_size=14)
            nx.draw_networkx_labels(nx_graph, pos_3, {node.id: str(node.id) for node in self.nodes_dict.values()}, font_size=5)
            node.set_color([colors[node.color] for node in self.nodes_dict.values()])
            node.set_edgecolor('black')

            plt.show()

    def copy(self):
        new_graph = Graph()
        new_graph.nodes_dict = {node_id: node.copy() for node_id, node in self.nodes_dict.items()}
        new_graph.nodes_with_color_assign = {new_graph.get_node_by_id(node.id) for node in self.nodes_with_color_assign}

        for original_node in self.nodes_dict.values():
            node_to_create_connection = new_graph.get_node_by_id(original_node.id)
            for original_node_connection in original_node.nodes_connected_to:
                node_to_connected = new_graph.get_node_by_id(original_node_connection.id)
                node_to_create_connection.nodes_connected_to.append(node_to_connected)

        return new_graph

    def get_return_format(self):
        return_node_list = [node for node in self.nodes_dict.values()]
        return_node_list.sort(key=lambda node: node.id)
        return_color_list = [node.color for node in return_node_list]
        return_string = ''
        return_string += str(len(set(return_color_list))) + ' 0 \n'
        return_string += ' '.join(map(str, return_color_list))
        return return_string

    @staticmethod
    def solve_graph_for_amount_of_colors(graph, color_pallet, node_selection_criteria, depth):
        if len(graph.nodes_dict) == len(graph.nodes_with_color_assign):
            return True
        attempt = 0
        max_attempts = max(8 - depth//10, 0)

        nodes_to_exclude = set(graph.nodes_with_color_assign)
        node = graph.get_node_under_criteria(node_selection_criteria, nodes_to_exclude)
        while node is not None and attempt <= max_attempts:
            color_of_surrounding_nodes = node.get_colors_of_surrounding_nodes()
            color = color_pallet.get_color(color_excluding=color_of_surrounding_nodes, selection='sequential')

            if color is None or color == 'None':
                print('Error')

            resolved_color_set = graph.set_color_of_node(node.id, color)
            if not resolved_color_set:
                index_of_node_assignation = graph.nodes_with_color_assign.index(node)
                nodes_ids_to_reset = [*map(lambda node_to_reset: node_to_reset.id, graph.nodes_with_color_assign[index_of_node_assignation:])]
                graph.reset_nodes_list(nodes_ids_to_reset)
                nodes_to_exclude.add(node)
                node = graph.get_node_under_criteria(node_selection_criteria, nodes_to_exclude)
            else:
                resolve_sub_problem = Graph.solve_graph_for_amount_of_colors(graph, color_pallet, node_selection_criteria, depth + 1)
                if resolve_sub_problem:
                    if '-1' in graph.get_return_format():
                        print('error')
                    return True
                else:
                    index_of_node_assignation = graph.nodes_with_color_assign.index(node)
                    nodes_ids_to_reset = [*map(lambda node_to_reset: node_to_reset.id, graph.nodes_with_color_assign[index_of_node_assignation:])]
                    graph.reset_nodes_list(nodes_ids_to_reset)
                    nodes_to_exclude.add(node)
                    node = graph.get_node_under_criteria(node_selection_criteria, nodes_to_exclude)
            attempt += 1
        return False
