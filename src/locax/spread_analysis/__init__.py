class SpreadAnalysis:

    def __init__(self, persons):
        self._spread_minimum_distance = 0.02  # In kilometers
        self._spread_minimum_duration = 60  # In seconds

        self._persons = persons

        # timestamps over which the analysis is happening
        self._timestamps = self._get_timestamps_to_consider()

        # distance matrix between persons identified by their ids at a specific
        # timestamp
        self._distances = {}

        # just initializing the distances to be sure that the different keys are
        # existing
        for person in self._persons:
            self._distances[person.id] = {}
            for to_person in self._persons:
                self._distances[person.id][to_person.id] = -1

    def detect_crossings(self, print_progression=None):
        for timestamp in self._timestamps:
            self._update_distances(timestamp)
            self._update_crossings(timestamp)

            if print_progression:
                progression = float(self._timestamps.index(timestamp)) / \
                              len(self._timestamps)
                print(progression)

        # we do this to force the crossing analysis to mark
        # valid spread (we need to end every crossing for this process to
        # happen
        for person in self._persons:
            self._distances[person.id] = {}
            for to_person in self._persons:
                self._distances[person.id][to_person.id] = \
                    self._spread_minimum_distance * 2

        one_minute = 60
        self._update_crossings(self._timestamps[-1] + one_minute)

    def _get_timestamps_to_consider(self):
        raw_timestamps = []
        for person in self._persons:
            for location in person.locations:
                raw_timestamps.append(location['timestampMs'] / 1000)

        raw_timestamps.sort()

        timestamps = []

        timestamp_delta_threshold = self._spread_minimum_duration / 2
        for raw_timestamp in raw_timestamps:
            delta = None
            if len(timestamps) >= 1:
                delta = raw_timestamp - timestamps[-1]

            if delta is not None and (delta < timestamp_delta_threshold):
                continue

            timestamps.append(raw_timestamp)

        return timestamps

    def _update_distances(self, timestamp):
        for person in self._persons:
            for to_person in self._persons:
                if person.id < to_person.id:
                    continue

                distance = person.distance_to_person_at_timestamp(
                    to_person, timestamp)
                self._distances[person.id][to_person.id] = distance
                self._distances[to_person.id][person.id] = distance

    def _update_crossings(self, timestamp):
        for person in self._persons:
            for to_person in self._persons:
                if person.id <= to_person.id:
                    continue

                self._update_crossing(person, to_person, timestamp)

    def _update_crossing(self, person, to_person, timestamp):
        distance = self._distances[person.id][to_person.id]

        is_crossing = distance < self._spread_minimum_distance

        crossing = person.consider_crossing_with(
            to_person, is_crossing, timestamp)
        self._mark_crossing_has_valid_spread(crossing)
        to_person_crossing = \
            to_person.consider_crossing_with(person, is_crossing,
                                             timestamp)
        self._mark_crossing_has_valid_spread(to_person_crossing)

    def _mark_crossing_has_valid_spread(self, crossing):
        if crossing is None:
            return

        crossing_has_ended = crossing.end_timestamp is not None
        if not crossing_has_ended:
            return

        valid_spread = crossing.get_duration() > self._spread_minimum_duration
        crossing.valid_spread = valid_spread and crossing.is_infectious

        if crossing.valid_spread:
            for person in crossing.persons:
                person.is_infected = True


if __name__ == '__main__':
    from locax.person_loader import load_persons

    persons = load_persons()

    spread_analysis = SpreadAnalysis(persons)
    spread_analysis.detect_crossings()