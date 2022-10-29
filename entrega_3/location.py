import math
import numpy as np

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
    def nearest_points_from_groups(loc_group_1: list, loc_group_2: list, exclude_loc=None):
        selected_tuple = None
        smallest_dist = float('inf')
        exclude_loc = [] if exclude_loc is None else exclude_loc

        if len(loc_group_1) == 1 and len(set(loc_group_1) - set(exclude_loc)) == 0:
            exclude_loc.remove(loc_group_1[0])
        if len(loc_group_2) == 1 and len(set(loc_group_2) - set(exclude_loc)) == 0:
            exclude_loc.remove(loc_group_2[0])

        for loc_1 in loc_group_1:
            for loc_2 in loc_group_2:
                if loc_1 not in exclude_loc and loc_2 not in exclude_loc:
                    if loc_1.distance_to_loc(loc_2) < smallest_dist:
                        smallest_dist = loc_1.distance_to_loc(loc_2)
                        selected_tuple = (loc_1, loc_2)
        return selected_tuple
