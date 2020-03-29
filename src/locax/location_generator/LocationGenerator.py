import random
import time
import datetime


class LocationGenerator:
    """
    This class should generate a location history for a single person.

    A person has a dwelling / home which is their base point
    A person has between 3 to 4 key points of interest
    A person has 10 secondary points of interest
    """

    def __init__(self, context):
        self._context = context

        self._home = self._context.get_random_point('home')

        number_of_key_points_of_interest = random.randint(3, 4)
        self._key_points_of_interest = \
            context.generate_random_points_of_interest(
                number_of_key_points_of_interest)

        number_of_secondary_points_of_interest = 10
        self._secondary_points_of_interest = \
            context.generate_random_points_of_interest(
                number_of_secondary_points_of_interest)

    def get_day_data(self, days_ago):
        current_poi = self._home
        current_timestamp = time.time()
        day_data = [self._get_location_data(
            current_poi, current_timestamp, 'home')]
        one_day_in_seconds = 24 * 60 * 60
        x_days_ago_timestamp = current_timestamp - days_ago * one_day_in_seconds
        x_days_ago_datetime = \
            datetime.datetime.fromtimestamp(x_days_ago_timestamp)

        midnight_datetime = \
            datetime.datetime.combine(x_days_ago_datetime, datetime.time.min)
        midnight_timestamp = int(midnight_datetime.strftime("%s"))
        one_day = (24 * 60 * 60)
        elapsed_time = 6 * 60 * 60

        points_of_interests_to_visit = \
            self._get_points_of_interest_to_visit_over_one_day()
        time_to_switch_location = random.randint(10 * 60, 50 * 60)
        mean_time_to_wait_at_location = (one_day - elapsed_time) / \
            len(points_of_interests_to_visit) \
            - time_to_switch_location

        for points_of_interests_index in \
                range(0, len(points_of_interests_to_visit)):

            next_poi = points_of_interests_to_visit.pop()
            timestamp_precision = 30
            move_timestamp = midnight_timestamp + elapsed_time + \
                mean_time_to_wait_at_location
            end_timestamp = move_timestamp \
                + int(time_to_switch_location / timestamp_precision) \
                * timestamp_precision
            timestamp_range = range(move_timestamp,
                                    end_timestamp + timestamp_precision,
                                    timestamp_precision)
            for intermediate_timestamp in timestamp_range:
                current_position = \
                    self._get_intermediate_location(
                        current_poi, next_poi,
                        move_timestamp, end_timestamp, intermediate_timestamp)
                location_name = 'moving-from-' + current_poi['name'] + \
                                '-to-' + next_poi['name']
                day_data.append(self._get_location_data(
                    current_position, intermediate_timestamp, location_name))

            current_poi = next_poi
            elapsed_time = end_timestamp - midnight_timestamp

        return day_data

    def _get_location_data(self, point, timestamp, name):
        return {
            'timestamp': timestamp,
            'x': point['x'],
            'y': point['y'],
            'name': name
        }

    def _get_points_of_interest_to_visit_over_one_day(self):
        """
        1 to 4 visited places
        Probability for one place to be a key point of interest: 3/5
        Probability for one place to be a secondary point of interest: 1/5
        Probability for one place to be a random point of interest: 1/5
        :return:
        """
        number_of_visited_places = random.randint(1, 4)

        points_of_interest_for_today = []

        for _ in range(0, number_of_visited_places):
            random_number = random.randint(1, 5)
            if random_number < 4:
                random.shuffle(self._key_points_of_interest)
                points_of_interest_for_today.append(
                    self._key_points_of_interest[0])
                continue

            if random_number < 5:
                random.shuffle(self._secondary_points_of_interest)
                points_of_interest_for_today.append(
                    self._secondary_points_of_interest[0])
                continue

            random.shuffle(self._context.points_of_interest)
            points_of_interest_for_today.append(
                self._context.points_of_interest[0])

        return points_of_interest_for_today

    def _get_intermediate_location(
            self,
            start_location,
            end_location,
            start_timestamp,
            end_timestamp,
            current_timestamp
    ):
        delta = float(end_timestamp - start_timestamp)
        progression = 1.0 - ((end_timestamp - current_timestamp) / delta)

        delta_x = (end_location['x'] - start_location['x'])
        x = start_location['x'] + delta_x * progression

        delta_y = (end_location['y'] - start_location['y'])
        y = start_location['y'] + delta_y * progression

        return {
            'x': x,
            'y': y,
        }
