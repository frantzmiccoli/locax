import random

seed = 644
random.seed(seed)


import math
import numpy
from pprint import pprint

from locax.location_generator.LocationGeneratorContext \
    import LocationGeneratorContext
from locax.location_generator.LocationGenerator import LocationGenerator

location_generator_context = LocationGeneratorContext()
location_generator = LocationGenerator(location_generator_context)


def test_init():
    assert('x' in location_generator._home)
    assert(len(location_generator._key_points_of_interest) < 5)
    assert(len(location_generator._secondary_points_of_interest) < 15)


def test_get_day_data_short_distance_between_points():
    day_data = location_generator.get_day_data(1)

    distances = []
    last_day_datum = None
    for day_datum in day_data:
        if last_day_datum is None:
            last_day_datum = day_datum
            continue

        delta_x = day_datum['x'] - last_day_datum['x']
        delta_y = day_datum['y'] - last_day_datum['y']
        distance = math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))
        distances.append(distance)
        last_day_datum = day_datum

    non_zero_distances = [d for d in distances if d > 0]
    assert(float(len(non_zero_distances)) / float(len(distances)) > 0.95)
    assert(numpy.std(distances) < 0.5)


def test_get_day_data_starts_and_ends_at_home():
    day_data = location_generator.get_day_data(1)

    distances_to_home = []
    day_data_to_consider = [day_data[0], day_data[-1]]  # first and last days
    for day_datum in day_data_to_consider:
        delta_x = day_datum['x'] - location_generator._home['x']
        delta_y = day_datum['y'] - location_generator._home['y']

        distance = math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))
        distances_to_home.append(distance)

    epsilon = 0.0000001
    non_zero_distances = [d for d in distances_to_home if abs(d) > epsilon]
    assert(len(non_zero_distances) == 0)


def test_get_day_data_stays_within_one_day():
    for i in range(0, 1000):
        local_location_generator_context = LocationGeneratorContext()
        local_location_generator = \
            LocationGenerator(local_location_generator_context)
        day_data = local_location_generator.get_day_data(1)
        first_day_data_timestamp = day_data[0]['timestamp']
        last_day_data_timestamp = day_data[-1]['timestamp']
        timestamp_difference = \
            last_day_data_timestamp - first_day_data_timestamp
        assert(timestamp_difference > 0)
        one_day = 24 * 60 * 60
        assert(timestamp_difference < one_day)


