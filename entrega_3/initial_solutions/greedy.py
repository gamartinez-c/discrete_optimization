import random

from location import Location
from initial_solution import InitialSolution


class Greedy(InitialSolution):

    def solve(self):
        first_location = self.first_location if self.first_location is not None else random.choice(self.locations_list)
        locations_return_list = []

        remaining_locations_to_add_in_sequence = self.locations_list.copy()
        picked_location = first_location

        locations_return_list.append(picked_location)
        remaining_locations_to_add_in_sequence.remove(picked_location)

        prev_location: Location
        prev_location = picked_location
        while len(remaining_locations_to_add_in_sequence) != 0:
            picked_location = prev_location.get_nearest_location(self.locations_list, exclude_location_list=locations_return_list)

            locations_return_list.append(picked_location)
            remaining_locations_to_add_in_sequence.remove(picked_location)

            prev_location = picked_location
        return locations_return_list
