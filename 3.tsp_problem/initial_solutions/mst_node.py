class MSTNode:

    def __init__(self, location):
        self.location = location

        self.child_nodes = []

    def get_l_to_r_node_path(self, preexisting_loc_list):
        if len(self.child_nodes) == 0:
            return preexisting_loc_list
        for child_node in self.child_nodes:
            preexisting_loc_list.append(child_node.location)
            preexisting_loc_list = child_node.get_l_to_r_node_path(preexisting_loc_list)
        return preexisting_loc_list

    def __str__(self):
        return str(self.location.id)

    def __repr__(self):
        return str(self.location.id)

