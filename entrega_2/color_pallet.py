import random


class ColorPallet:
    def __init__(self, initial_color_count=None):
        if initial_color_count is None:
            initial_color_count = 1
        self.colors = [*range(initial_color_count)]

    def get_color(self, color_excluding=None, selection='random'):
        color_excluding = [] if color_excluding is None else color_excluding
        color_to_choose_from = set(self.colors) - set(color_excluding)
        if len(color_to_choose_from) == 0:
            return None
        elif selection == 'random':
            return random.choice([*color_to_choose_from])
        elif selection == 'sequential':
            color_to_choose_from = list(color_to_choose_from)
            color_to_choose_from.sort()
            return color_to_choose_from[0]
        else:
            color = self.get_next_sequential_color()
            while color in color_excluding:
                color = self.get_next_sequential_color()
            return color

    def get_next_sequential_color(self):
        counter = 0
        while True:
            index = counter % len(self.colors)
            print(counter, index)
            yield self.colors[index]
            counter += 1

    def add_color(self):
        color = len(self.colors)
        self.colors.append(color)
        return color

    def __len__(self):
        return len(self.colors)
