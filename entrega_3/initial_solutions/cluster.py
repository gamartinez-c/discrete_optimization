import pandas as pd
from sklearn.cluster import KMeans

from location import Location
from initial_solutions.greedy import Greedy
from initial_solutions.initial_solution import InitialSolution


class Cluster(InitialSolution):

    def __init__(self, locations_list, first_location, type_of_assignation=1):
        super().__init__(locations_list, first_location)
        self.type_of_assignation = type_of_assignation

    def solve(self):
        info_dict = {'id': [], 'x': [], 'y': []}
        for location in self.locations_list:
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
        while (amount_of_clusters < 2 or relative_distance > 0.1) and amount_of_clusters < (len(self.locations_list) - 1):
            amount_of_clusters += 4
            kmeans = KMeans(n_clusters=amount_of_clusters)
            kmeans.fit(x)
            k_distances.append(kmeans.inertia_)
            relative_distance = (k_distances[-1] / k_distances[0])

        info_df['cluster'] = kmeans.labels_
        clusters = info_df[['id', 'cluster']].groupby('cluster').apply(lambda cluster: list(cluster['id'])).to_dict()
        clusters = {cluster_id: [self.locations_list[location_id] for location_id in locations_ids] for cluster_id, locations_ids in clusters.items()}

        # Find the sorting of clusters in a big picture.
        cluster_locations_original = [Location(x, y, add_to_static=False) for x, y in kmeans.cluster_centers_]
        for i, loc in enumerate(cluster_locations_original):
            loc.id = i

        for location in cluster_locations_original:
            locations_to_order = [loc for loc in cluster_locations_original if loc != location]
            location.location_order_by_distance = [loc for loc in location.get_sorted_list_of_loc(locations_to_order)]

        cluster_locations_to_sort = cluster_locations_original.copy()
        # cluster_locations_to_sort = Location.greedy_of_less_adding_cost(cluster_locations_to_sort)
        # FIXME
        cluster_locations_to_sort = Greedy(cluster_locations_to_sort)
        # Location.get_locations_ordered_by_distance(cluster_locations_to_sort)

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
            try:
                end_connection[current_cluster_label] = nearest_tuple[0]
            except:
                Location.nearest_points_from_groups(clusters[current_cluster_label], clusters[following_cluster_label], exclude_loc=exclude_loc)
            start_connector[following_cluster_label] = nearest_tuple[1]

        sorted_cluster_dict = {}
        for cluster_label in clusters:
            self.locations_list = clusters[cluster_label]
            start_loc = start_connector[cluster_label]
            if self.type_of_assignation == 1:
                end_loc = end_connection[cluster_label]
                sorted_cluster_dict[cluster_label] = Location.greedy_of_less_adding_cost(self.locations_list, start_loc, end_loc)
            else:
                sorted_cluster_dict[cluster_label] = Location.get_locations_ordered_by_distance(self.locations_list, first_location=start_loc)

        final_location_list = []
        for cluster_loc in cluster_locations_to_sort[:-1]:
            cluster_label = cluster_locations_original.index(cluster_loc)
            final_location_list += sorted_cluster_dict[cluster_label]

        return final_location_list
