from route import Route
from initial_solution import InitialSolution


class LessAddingCost(InitialSolution):

    def solve(self, start_loc=None, end_loc=None):
        all_locations_to_consider = [*self.locations_list]
        temporary_route = Route(all_locations_to_consider.copy())

        starter_index = 0 if start_loc is None else 1
        end_index = len(all_locations_to_consider) if end_loc is None else len(all_locations_to_consider) - 1

        if start_loc is not None:
            self.locations_list.remove(start_loc)
            temporary_route.add_location(start_loc)
        if end_loc is not None:
            self.locations_list.remove(end_loc)
            temporary_route.add_location(end_loc, index=len(temporary_route))

        for loc in self.locations_list:
            best_index = None
            best_val = float('inf')
            for index in range(0, len(temporary_route) + 1, 3):
                # Fixme place if instead.
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