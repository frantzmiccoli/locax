import random


class LocationGeneratorContext:

    def __init__(self):
        self.min_x = 0
        self.max_x = 100
        self.min_y = 0
        self.max_y = 100

        self.points_of_interest = []
        self._generate_points_of_interest()

    def get_random_point(self, name):
        point_of_interest = {
            'x': self._get_random_value(self.min_x, self.max_x),
            'y': self._get_random_value(self.min_y, self.max_y),
            'name': name
        }
        return point_of_interest

    def _generate_points_of_interest(self):
        number_of_points_of_interests_to_generate = 100

        for i in range(0, number_of_points_of_interests_to_generate):
            name = 'poi-' + i
            self.points_of_interest.append(self.get_random_point(name))

    def _get_random_value(self, min_value, max_value):
        delta = max_value - min_value
        random_value = min_value + random.random() * delta
        return random_value
