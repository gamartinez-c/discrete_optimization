import math
import random
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from mst_node import MSTNode
from route import Route


class Location:
    count_of_locations = 0

    locations_list = []

    def __init__(self, x, y, add_to_static=True):
        self.id = Location.count_of_locations

        self.x = x
        self.y = y

        self.location_order_by_distance = []

        Location.count_of_locations += 1
        if add_to_static:
            Location.locations_list.append(self)

    def distance_to_loc(self, other_location=None):
        if other_location is not None:
            x_distance = self.x - other_location.x
            y_distance = self.y - other_location.y
        else:
            x_distance = self.x
            y_distance = self.y
        distance = math.sqrt(x_distance**2 + y_distance**2)
        return distance

    def distance_to_pos(self, x=0, y=0):
        x_distance = self.x - x
        y_distance = self.y - y
        distance = math.sqrt(x_distance**2 + y_distance**2)
        return distance

    def get_nearest_location(self, locations_list, exclude_location_list=None):
        return_location = None
        for location in self.location_order_by_distance:
            if location not in exclude_location_list and location in locations_list:
                return location
        return return_location

    def angle_with_location(self, other_location=None):
        relative_x = other_location.x - self.x if other_location is not None else -self.x
        relative_y = other_location.y - self.y if other_location is not None else -self.y
        ang1 = (-np.arctan2(relative_x, relative_y) + np.pi) % (np.pi*2)
        return np.rad2deg(ang1)

    def sort_location_list_by_distance(self, location_order_by_id):
        self.location_order_by_distance = self.get_sorted_list_of_loc(self.location_order_by_distance)

    def get_sorted_list_of_loc(self, list_of_locations):
        list_of_locations.sort(key=lambda loc: self.distance_to_loc(loc))
        return list_of_locations

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def get_locations_ordered_by_distance(locations_list, first_location=None):
        first_location = first_location if first_location is not None else random.choice(locations_list)
        locations_return_list = []

        remaining_locations_to_add_in_sequence = locations_list.copy()
        picked_location = first_location

        locations_return_list.append(picked_location)
        remaining_locations_to_add_in_sequence.remove(picked_location)

        prev_location: Location
        prev_location = picked_location
        while len(remaining_locations_to_add_in_sequence) != 0:
            picked_location = prev_location.get_nearest_location(locations_list, exclude_location_list=locations_return_list)

            locations_return_list.append(picked_location)
            remaining_locations_to_add_in_sequence.remove(picked_location)

            prev_location = picked_location
        return locations_return_list

    @staticmethod
    def get_locations_ordered_by_anti_clockwise(locations_list, first_location=None):
        first_location = first_location if first_location is not None else random.choice(locations_list)
        locations_return_list = []

        remaining_locations_to_add_in_sequence = locations_list.copy()
        picked_location = first_location
        prev_angle = 0

        locations_return_list.append(picked_location)
        remaining_locations_to_add_in_sequence.remove(picked_location)

        angle_offset = 0
        while len(remaining_locations_to_add_in_sequence) != 1:
            picked_location = remaining_locations_to_add_in_sequence[0]
            min_angle_of_picked = locations_return_list[-1].angle_with_location(picked_location)
            min_angle_of_picked_relative_to_offset = (min_angle_of_picked - angle_offset) % 360
            for location in remaining_locations_to_add_in_sequence[1:]:
                angle_to_prev_location = locations_return_list[-1].angle_with_location(location)
                angle_to_prev_location_relative_to_offset = (angle_to_prev_location - angle_offset) % 360
                if min_angle_of_picked_relative_to_offset > angle_to_prev_location_relative_to_offset:
                    picked_location = location
                    min_angle_of_picked = angle_to_prev_location
                    min_angle_of_picked_relative_to_offset = (min_angle_of_picked - angle_offset) % 360

            locations_return_list.append(picked_location)
            remaining_locations_to_add_in_sequence.remove(picked_location)

            while min_angle_of_picked < angle_offset:
                min_angle_of_picked += 360
            if (min_angle_of_picked - angle_offset) > 180:
                angle_offset += max((np.ceil((min_angle_of_picked - angle_offset) / 90) - 2)*90, 0)

            # set offset if needed

        picked_location = remaining_locations_to_add_in_sequence[0]
        locations_return_list.append(picked_location)

        return locations_return_list

    @staticmethod
    def get_mst(locations_list, first_location=None):
        first_location = first_location if first_location is not None else random.choice(locations_list)
        selected_locations = [first_location]
        base_node = MSTNode(first_location)
        nodes_dict = {first_location: base_node}

        dict_loc_and_short_loc_to = {loc: loc.location_order_by_distance.copy() for loc in locations_list}
        for loc in dict_loc_and_short_loc_to:
            if first_location in dict_loc_and_short_loc_to[loc]:
                dict_loc_and_short_loc_to[loc].remove(first_location)

        while len(selected_locations) != len(locations_list):
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

    @staticmethod
    def get_random_location_list(location_return_list):
        random.shuffle(location_return_list)
        return location_return_list

    @staticmethod
    def get_nearest_location_to_location(locations_list, x=0, y=0):
        first_location = locations_list[0]
        min_distance = first_location.distance_to_pos(x=x, y=y)
        for location in locations_list[1:]:
            if location.distance_to_loc() < min_distance:
                first_location = location
                min_distance = location.distance_to_pos(x=x, y=y)
        return first_location

    @staticmethod
    def load_locations(position_list):
        Location.locations_list = []
        Location.count_of_locations = 0
        for locations_line in position_list:
            parts = locations_line.split()
            new_location = Location(float(parts[0]), float(parts[1]))

            for location in Location.locations_list:
                if location != new_location:
                    location.location_order_by_distance.append(new_location)
                    new_location.location_order_by_distance.append(location)
        location_list = Location.locations_list.copy()
        return location_list

    @staticmethod
    def get_clustered_locations_solution(locations_list, first_location=None):
        info_dict = {'id': [], 'x': [], 'y': []}
        for location in locations_list:
            info_dict['id'].append(location.id)
            info_dict['x'].append(location.x)
            info_dict['y'].append(location.y)
        info_df = pd.DataFrame(info_dict)
        x = info_df[['x', 'y']].values

        k_distances = []
        relative_distance = 1
        amount_of_clusters = 1
        kmeans = KMeans(n_clusters=amount_of_clusters)
        kmeans.fit(x)
        k_distances.append(kmeans.inertia_)
        while (amount_of_clusters < 2 or relative_distance > 0.1) and amount_of_clusters < (len(locations_list) - 1):
            amount_of_clusters += 1
            kmeans = KMeans(n_clusters=amount_of_clusters)
            kmeans.fit(x)
            k_distances.append(kmeans.inertia_)
            relative_distance = (k_distances[-1] / k_distances[0])

        info_df['cluster'] = kmeans.labels_
        clusters = info_df[['id', 'cluster']].groupby('cluster').apply(lambda cluster: list(cluster['id'])).to_dict()
        clusters = {cluster_id: [locations_list[location_id] for location_id in locations_ids] for cluster_id, locations_ids in clusters.items()}

        # Find the sorting of clusters in a big picture.
        cluster_locations_original = [Location(x, y, add_to_static=False) for x, y in kmeans.cluster_centers_]
        for i, loc in enumerate(cluster_locations_original):
            loc.id = i

        for location in cluster_locations_original:
            locations_to_order = [loc for loc in cluster_locations_original if loc != location]
            location.location_order_by_distance = [loc for loc in location.get_sorted_list_of_loc(locations_to_order)]

        cluster_locations_to_sort = cluster_locations_original.copy()
        # cluster_locations_to_sort = Location.greedy_of_less_adding_cost(cluster_locations_to_sort)
        cluster_locations_to_sort = Location.get_locations_ordered_by_distance(cluster_locations_to_sort)

        # Find which of each cluster will be connected to each other loc of other cluster.
        start_connector = {}
        end_connection = {}
        cluster_locations_to_sort.append(cluster_locations_to_sort[0])
        for i in range(len(cluster_locations_to_sort)-1):
            current_cluster = cluster_locations_to_sort[i]
            following_cluster = cluster_locations_to_sort[i+1]

            current_cluster_label = cluster_locations_original.index(current_cluster)
            following_cluster_label = cluster_locations_original.index(following_cluster)

            exclude_loc = []
            for cluster_label_bis in (current_cluster_label, following_cluster_label):
                for dict_connector in (start_connector, end_connection):
                    if cluster_label_bis in dict_connector:
                        exclude_loc.append(dict_connector[cluster_label_bis])

            nearest_tuple = Location.nearest_points_from_groups(clusters[current_cluster_label], clusters[following_cluster_label], exclude_loc=exclude_loc)
            end_connection[current_cluster_label] = nearest_tuple[0]
            start_connector[following_cluster_label] = nearest_tuple[1]

        sorted_cluster_dict = {}
        for cluster_label in clusters:
            locations_list = clusters[cluster_label]
            start_loc = start_connector[cluster_label]
            if first_location == 1:
                end_loc = end_connection[cluster_label]
                sorted_cluster_dict[cluster_label] = Location.greedy_of_less_adding_cost(locations_list, start_loc, end_loc)
            else:
                sorted_cluster_dict[cluster_label] = Location.get_locations_ordered_by_distance(locations_list, first_location=start_loc)

        final_location_list = []
        for cluster_loc in cluster_locations_to_sort[:-1]:
            cluster_label = cluster_locations_original.index(cluster_loc)
            final_location_list += sorted_cluster_dict[cluster_label]

        return final_location_list

    @staticmethod
    def nearest_points_from_groups(loc_group_1: list, loc_group_2: list, exclude_loc=None):
        selected_tuple = None
        smallest_dist = float('inf')
        exclude_loc = [] if exclude_loc is None else exclude_loc

        for loc_1 in loc_group_1:
            for loc_2 in loc_group_2:
                if loc_1 not in exclude_loc and loc_2 not in exclude_loc:
                    if loc_1.distance_to_loc(loc_2) < smallest_dist:
                        smallest_dist = loc_1.distance_to_loc(loc_2)
                        selected_tuple = (loc_1, loc_2)
        return selected_tuple

    @staticmethod
    def greedy_of_less_adding_cost(locations_list, start_loc=None, end_loc=None):
        all_locations_to_consider = [*locations_list]
        temporary_route = Route(all_locations_to_consider.copy())

        starter_index = 0 if start_loc is None else 1
        end_index = len(all_locations_to_consider) if end_loc is None else len(all_locations_to_consider) - 1

        if start_loc is not None:
            locations_list.remove(start_loc)
            temporary_route.add_location(start_loc)
        if end_loc is not None:
            locations_list.remove(end_loc)
            temporary_route.add_location(end_loc, index=len(temporary_route))

        for loc in locations_list:
            best_index = None
            best_val = float('inf')
            for index in range(len(temporary_route) + 1):
                index_to_insert = max(starter_index, index)
                index_to_insert = min(index_to_insert, end_index)
                temporary_route.add_location(loc, index=index_to_insert)

                cost_of_insertion = temporary_route.get_total_distance_of_location(index_to_insert)
                if cost_of_insertion < best_val:
                    best_index = index_to_insert
                    best_val = cost_of_insertion

                temporary_route.remove_location(loc)

            temporary_route.add_location(loc, best_index)
        return list(temporary_route.sequence_list)
