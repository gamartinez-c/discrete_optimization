from location import Location


class InitialSolution:

    def __init__(self, locations_list: list[Location], first_location: Location = None):
        self.locations_list = locations_list
        self.first_location = first_location
        self.route = None

    def get_solution(self):
        return self.route
