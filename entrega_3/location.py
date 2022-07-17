import math
import random
import numpy as np


class Location:
    count_of_locations = 0

    locations_list = []

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.id = Location.count_of_locations

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
        locations_to_compare = Location.locations_list.copy()
        locations_to_compare.remove(self)
        if exclude_location_list is not None:
            for location in exclude_location_list:
                locations_to_compare.remove(location)

        if len(locations_to_compare) == 0:
            return None
        else:
            picked_location = locations_to_compare[0]
            min_distance = self.distance_to(picked_location)
            for location in locations_to_compare[1:]:
                distance_to_location = self.distance_to(location)
                if distance_to_location < min_distance:
                    picked_location = location
                    min_distance = distance_to_location
            return picked_location, min_distance

    def angle_with_location(self, other_location=None):
        relative_x = other_location.x - self.x if other_location is not None else -self.x
        relative_y = other_location.y - self.y if other_location is not None else -self.y
        print(relative_x, relative_y)
        print((-np.arctan2(relative_x, relative_y) + np.pi), (-np.arctan2(relative_x, relative_y) + np.pi)% (np.pi*2))
        ang1 = (-np.arctan2(relative_x, relative_y) + np.pi/2) % (np.pi*2)
        return np.rad2deg(ang1)

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

        while len(remaining_locations_to_add_in_sequence) != 1:
            picked_location = remaining_locations_to_add_in_sequence[0]
            min_distance_of_picked = picked_location.distance_to(locations_return_list[-1])
            for location in remaining_locations_to_add_in_sequence[1:]:
                distance_to_prev_location = location.distance_to(locations_return_list[-1])
                if min_distance_of_picked > distance_to_prev_location:
                    picked_location = location
                    min_distance_of_picked = distance_to_prev_location

            locations_return_list.append(picked_location)
            remaining_locations_to_add_in_sequence.remove(picked_location)

        picked_location = remaining_locations_to_add_in_sequence[0]
        locations_return_list.append(picked_location)

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

        while len(remaining_locations_to_add_in_sequence) != 1:
            picked_location = remaining_locations_to_add_in_sequence[0]
            min_angle_of_picked = locations_return_list[-1].angle_with_location(picked_location)
            less_turn = 360
            for location in remaining_locations_to_add_in_sequence[1:]:
                angle_to_prev_location = locations_return_list[-1].angle_with_location(location)
                if less_turn > (prev_angle - 20 - angle_to_prev_location):
                    picked_location = location
                    min_angle_of_picked = angle_to_prev_location
                    less_turn = (prev_angle - 20 - angle_to_prev_location)

            prev_angle = min_angle_of_picked
            locations_return_list.append(picked_location)
            remaining_locations_to_add_in_sequence.remove(picked_location)

        picked_location = remaining_locations_to_add_in_sequence[0]
        locations_return_list.append(picked_location)

        return locations_return_list

    @staticmethod
    def get_random_location_list():
        location_return_list = Location.locations_list.copy()
        random.shuffle(location_return_list)
        return location_return_list