import json


def load_locations():
    target_path = \
        './locationData/Person-0/Location History/Location History.json'
    with open(target_path, 'r') as handle:
        return json.load(handle)['locations']


def get_location_at_timestamp(timestamp, locations):
    timestamp_ms = timestamp * 1000

    last_location = locations[0]
    for location in locations:
        if timestamp_ms < location['timestampMs']:
            break

        last_location = location

    return [
        last_location['latitudeE7'] / 10000000.,
        last_location['longitudeE7'] / 10000000.
    ]