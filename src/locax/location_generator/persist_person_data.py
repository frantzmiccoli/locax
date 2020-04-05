import os
import haversine
import numpy
import json


def persist_person_data(name, person_data):
    # Create the relevant file hierarchy
    target_path = os.path.join(
        './locationData/', name, 'Location History', 'Location History.json')
    target_dir = os.path.dirname(target_path)
    os.makedirs(target_dir)

    #Switch from x, y coordinates to latitude, longitude
    locations = []
    for data_point in person_data:
        location = {'timestampMs': data_point['timestamp'] * 1000}
        gps_coordinates = _get_gps_coordinates(data_point)
        location['latitudeE7'] = int(gps_coordinates[0] * 10000000)
        location['longitudeE7'] = int(gps_coordinates[1] * 10000000)
        locations.append(location)
    json_data = {'locations': locations}

    #Write json file
    with open(target_path, 'w') as handle:
        json.dump(json_data, handle, indent=4)


reference_point = (49.6116, 6.1319)  # Luxembourg

minor_delta = 0.1
latitude_tilted_point_1 = \
    (reference_point[0] + minor_delta, reference_point[1])
latitude_tilted_point_2 = \
    (reference_point[0] - minor_delta, reference_point[1])
latitude_distances = [
    haversine.haversine(reference_point, latitude_tilted_point_1),
    haversine.haversine(reference_point, latitude_tilted_point_2),
]

# km / coordinates unit
latitude_distance_ratio = numpy.average(latitude_distances) / minor_delta

longitude_tilted_point_1 = \
    (reference_point[0], reference_point[1] + minor_delta)
longitude_tilted_point_2 = \
    (reference_point[0], reference_point[1] + minor_delta)
longitude_distances = [
    haversine.haversine(reference_point, longitude_tilted_point_1),
    haversine.haversine(reference_point, longitude_tilted_point_2),
]

# km / coordinates unit
longitude_distance_ratio = numpy.average(longitude_distances) / minor_delta


span_in_km = 20.0


def _get_gps_coordinates(data_point):
    wished_distance_latitude = ((data_point['x'] - 50) * span_in_km) / 100
    latitude = reference_point[0] + \
               (wished_distance_latitude / latitude_distance_ratio)

    wished_distance_longitude = ((data_point['y'] - 50) * span_in_km) / 100
    longitude = reference_point[1] + \
               (wished_distance_longitude / longitude_distance_ratio)
    return (latitude, longitude)



