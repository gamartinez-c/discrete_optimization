import random
import numpy as np

from initial_solutions.initial_solution import InitialSolution


class Clock(InitialSolution):

    def solve(self):
        first_location = self.first_location if self.first_location is not None else random.choice(self.locations_list)
        locations_return_list = []

        remaining_locations_to_add_in_sequence = self.locations_list.copy()
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
