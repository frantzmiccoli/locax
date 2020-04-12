from haversine import haversine
from locax.model.Crossing import Crossing
import random


class Person:

    def __init__(self, person_id, name, locations):
        self.id = int(person_id)
        self.name = name
        self.locations = locations
        self.marker = None

        self.is_infected = random.randint(0, 99) <= 5

        self.crossings = []
        self._active_crossings = []

    def __str__(self):
        return 'Person: ' + self.name

    def get_location_at_timestamp(self, timestamp):
        timestamp_ms = timestamp * 1000

        last_location = self.locations[0]
        for location in self.locations:
            if timestamp_ms < location['timestampMs']:
                break

            last_location = location

        return [
            last_location['latitudeE7'] / 10000000.,
            last_location['longitudeE7'] / 10000000.
        ]

    def distance_to_person_at_timestamp(self, person, timestamp):
        if person.id == self.id:
            return 0.0
        location_1 = self.get_location_at_timestamp(timestamp)
        location_2 = person.get_location_at_timestamp(timestamp)
        return haversine(location_1, location_2)

    def consider_crossing_with(self, person, is_crossing, timestamp):
        active_crossing = self._get_active_crossing_with(person)

        if (active_crossing is None) and not is_crossing:
            # nothing is and nothing should be
            return None

        if (active_crossing is not None) and is_crossing:
            # this crossing is active and should be
            return active_crossing

        if is_crossing:  # I can deduce active_crossing is currently None
            active_crossing = Crossing(timestamp, [self, person])
            self.crossings.append(active_crossing)
            self._active_crossings.append(active_crossing)
            return active_crossing

        if not is_crossing:  # the active_crossing is over
            active_crossing.end_timestamp = timestamp
            self._active_crossings.remove(active_crossing)
            return active_crossing

    def has_valid_spread_at_timestamp(self, timestamp):
        for crossing in self.crossings:
            if not crossing.valid_spread:
                continue

            if crossing.start_timestamp < timestamp:
                return True

        return False

    def _get_active_crossing_with(self, person):
        for crossing in self._active_crossings:
            if not crossing.involves(person):
                continue

            return crossing

        return None
