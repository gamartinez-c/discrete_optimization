import math
import random
import numpy as np


class Location:
    count_of_locations = 0

    locations_list = []

    def __init__(self, x, y):
        self.id = Location.count_of_locations

        self.x = x
        self.y = y

        self.location_order_by_distance = []

        Location.locations_list.append(self)

        Location.count_of_locations += 1

    def distance_to(self, other_location=None):
        if other_location is not None:
            x_distance = self.x - other_location.x
            y_distance = self.y - other_location.y
        else:
            x_distance = self.x
            y_distance = self.y
        distance = math.sqrt(x_distance**2 + y_distance**2)
        return distance

    def get_nearest_location(self, exclude_location_list=None):
        return_location = None
        for location_id in self.location_order_by_distance:
            location = Location.locations_list[location_id]
            if location not in exclude_location_list:
                return location
        return return_location

    def angle_with_location(self, other_location=None):
        relative_x = other_location.x - self.x if other_location is not None else -self.x
        relative_y = other_location.y - self.y if other_location is not None else -self.y
        ang1 = (-np.arctan2(relative_x, relative_y) + np.pi) % (np.pi*2)
        return np.rad2deg(ang1)

    def sort_location_list_by_distance(self):
        self.location_order_by_distance = [Location.locations_list[loc_id] for loc_id in self.location_order_by_distance]
        self.location_order_by_distance.sort(key=lambda loc: self.distance_to(loc))
        self.location_order_by_distance = [loc.id for loc in self.location_order_by_distance]

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    @staticmethod
    def get_locations_ordered_by_distance(first_location=None):
        first_location = first_location if first_location is not None else random.choice(Location.locations_list)
        locations_return_list = []

        remaining_locations_to_add_in_sequence = Location.locations_list.copy()
        picked_location = first_location

        locations_return_list.append(picked_location)
        remaining_locations_to_add_in_sequence.remove(picked_location)

        prev_location: Location
        prev_location = picked_location
        while len(remaining_locations_to_add_in_sequence) != 0:
            picked_location = prev_location.get_nearest_location(exclude_location_list=locations_return_list)

            locations_return_list.append(picked_location)
            remaining_locations_to_add_in_sequence.remove(picked_location)

            prev_location = picked_location
        return locations_return_list

    @staticmethod
    def get_locations_ordered_by_anti_clockwise(first_location=None):
        first_location = first_location if first_location is not None else random.choice(Location.locations_list)
        locations_return_list = []

        remaining_locations_to_add_in_sequence = Location.locations_list.copy()
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
    def get_random_location_list():
        location_return_list = Location.locations_list.copy()
        random.shuffle(location_return_list)
        return location_return_list

    @staticmethod
    def get_nearest_location_to_origin():
        first_location = Location.locations_list[0]
        min_distance = first_location.distance_to()
        for location in Location.locations_list[1:]:
            if location.distance_to() < min_distance:
                first_location = location
                min_distance = location.distance_to()
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
                    location.location_order_by_distance.append(new_location.id)
                    new_location.location_order_by_distance.append(location.id)
