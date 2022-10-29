import random

from mst_node import MSTNode
from initial_solution import InitialSolution


class MST(InitialSolution):

    def solve(self):
        first_location = self.first_location if self.first_location is not None else random.choice(self.locations_list)
        selected_locations = [first_location]
        base_node = MSTNode(first_location)
        nodes_dict = {first_location: base_node}

        dict_loc_and_short_loc_to = {loc: loc.location_order_by_distance.copy() for loc in self.locations_list}
        for loc in dict_loc_and_short_loc_to:
            if first_location in dict_loc_and_short_loc_to[loc]:
                dict_loc_and_short_loc_to[loc].remove(first_location)

        while len(selected_locations) != len(self.locations_list):
            # From the tree we already have we go on picking the one connection that is the smallest
            selected_location = None
            selected_source = None
            dist_btw_selected_nodes = None
            for source_loc in selected_locations:
                dest_loc = dict_loc_and_short_loc_to[source_loc][0]
                dist_btw_nodes = source_loc.distance_to_loc(dest_loc)
                if dist_btw_selected_nodes is None or dist_btw_nodes < dist_btw_selected_nodes:
                    selected_location = dest_loc
                    selected_source = source_loc
                    dist_btw_selected_nodes = dist_btw_nodes

            # After selecting the node we expand the Tree
            selected_locations.append(selected_location)

            dest_node = MSTNode(selected_location)
            nodes_dict[selected_location] = dest_node

            source_node = nodes_dict[selected_source]
            source_node.child_nodes.append(dest_node)

            for loc in dict_loc_and_short_loc_to:
                if selected_location in dict_loc_and_short_loc_to[loc]:
                    dict_loc_and_short_loc_to[loc].remove(selected_location)

        locations_l_to_r_ist = base_node.get_l_to_r_node_path([base_node.location])
        return locations_l_to_r_ist
