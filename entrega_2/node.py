class Node:
    def __init__(self, node_id, possible_colors):
        self.id = node_id

        self.possible_colors = possible_colors.copy()
        self.original_possible_colors = possible_colors.copy()

        self.color = -1
        self.nodes_connected_to = list()

    def get_colors_of_surrounding_nodes(self):
        color_set = {neighbour.color for neighbour in self.nodes_connected_to}
        return color_set

    def get_amount_of_connections(self):
        return len(self.nodes_connected_to)

    def does_node_has_color(self):
        return self.color != -1

    def constrain_color(self, color):
        if color in self.possible_colors:
            self.possible_colors.remove(color)

    def copy(self):
        new_node = Node(self.id, self.possible_colors.copy())
        new_node.color = self.color
        return new_node

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self.id)
