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

