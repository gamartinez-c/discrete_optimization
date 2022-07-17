from location import Location
import matplotlib.pyplot as plt


class Route:
    def __init__(self):
        self.sequence_list = []

    def add_location(self, location, index=None):
        if index is None:
            self.sequence_list.append(location)
        elif index >= len(self.sequence_list):
            self.sequence_list.append(location)
        else:
            self.sequence_list.insert(index, location)

    def get_total_distance_travel(self):
        total_distance = 0
        if len(self.sequence_list) <= 1:
            return total_distance
        else:
            index = 0
            while index != (len(self.sequence_list) - 1):
                location_1 = self.sequence_list[index]
                location_2 = self.sequence_list[index + 1]
                total_distance += location_1.distance_to(location_2)
                index += 1
            location_1 = self.sequence_list[-1]
            location_2 = self.sequence_list[0]
            total_distance += location_1.distance_to(location_2)
            return total_distance

    def swap_locations(self, location_1, location_2):
        index_of_location_1 = self.sequence_list.index(location_1)
        index_of_location_2 = self.sequence_list.index(location_2)

        self.add_location(location_1, index_of_location_2)
        self.sequence_list.remove(location_2)

        self.add_location(location_2, index_of_location_1)
        self.sequence_list.remove(location_1)

    def plot_route(self):
        position_x_in_route = []
        position_y_in_route = []
        for location in self.sequence_list:
            position_x_in_route.append(location.x)
            position_y_in_route.append(location.y)
        plt.plot(position_x_in_route, position_y_in_route, color='black', marker='o')
        if len(self.sequence_list) == len(Location.locations_list):
            position_x_in_route = []
            position_y_in_route = []
            for location in [self.sequence_list[0], self.sequence_list[-1]]:
                position_x_in_route.append(location.x)
                position_y_in_route.append(location.y)
                plt.plot(position_x_in_route, position_y_in_route, color='red')

        locations_not_in_route = set(Location.locations_list) - set(self.sequence_list)
        position_x_not_in_route = []
        position_y_not_in_route = []
        for location in locations_not_in_route:
            position_x_not_in_route.append(location.x)
            position_y_not_in_route.append(location.y)
        plt.scatter(position_x_not_in_route, position_y_not_in_route, color='black', marker='o')

        for location in Location.locations_list:
            x, y, s = location.x, location.y, location.id
            plt.text(x+1, y+1, s)

        plt.show()
