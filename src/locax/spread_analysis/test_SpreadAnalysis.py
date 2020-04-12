from locax.spread_analysis import SpreadAnalysis
from locax.model.Person import Person


def test_detect_crossings():
    persons = []
    name_counter = 0
    fake_locations = _get_fake_locations()
    for fake_location in fake_locations:
        name = 'Person-' + str(name_counter)
        persons.append(Person(name_counter, name, fake_location))
        name_counter += 1

    persons[2].is_infected = True

    spread_analysis = SpreadAnalysis(persons)
    spread_analysis.detect_crossings()

    person_0 = persons[0]
    assert(len(person_0.crossings) == 1)
    person_1 = persons[1]
    assert(len(person_1.crossings) == 2)
    person_2 = persons[2]
    assert(len(person_2.crossings) == 1)

    person_1_crossings = person_1.crossings
    crossing_with_person_2 = person_1_crossings[-1]
    assert(crossing_with_person_2.valid_spread)


def _get_fake_locations():
    timestamp_scale = 180000

    fake_location_1 = [
        {
            'timestampMs': 0,
            'latitudeE7':  49.598799 * 10000000,
            'longitudeE7': 6.125781 * 10000000,
        },
        {
            'timestampMs': timestamp_scale,
            'latitudeE7':  49.598799 * 10000000,
            'longitudeE7': 6.125781 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 2,
            'latitudeE7':  49.598799 * 10000000,
            'longitudeE7': 6.125781 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 3,
            'latitudeE7':  49.598799 * 10000000,
            'longitudeE7': 6.125781 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 4,
            'latitudeE7':  49.598799 * 10000000,
            'longitudeE7': 6.125781 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 5,
            'latitudeE7':  49.598799 * 10000000,
            'longitudeE7': 6.125781 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 6,
            'latitudeE7':  49.598799 * 10000000,
            'longitudeE7': 6.125781 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 7,
            'latitudeE7':  49.598799 * 10000000,
            'longitudeE7': 6.125781 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 8,
            'latitudeE7':  49.598799 * 10000000,
            'longitudeE7': 6.125781 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 9,
            'latitudeE7':  49.598799 * 10000000,
            'longitudeE7': 6.125781 * 10000000,
        }
    ]

    fake_location_2 = [
        {
            'timestampMs': 0,
            'latitudeE7': 49.598799 * 10000000,
            'longitudeE7': 6.125781 * 10000000,
        },
        {
            'timestampMs': timestamp_scale,
            'latitudeE7': 49.598736 * 10000000,
            'longitudeE7': 6.127228 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 2,
            'latitudeE7': 49.598486 * 10000000,
            'longitudeE7': 6.598799 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 3,
            'latitudeE7': 49.598409 * 10000000,
            'longitudeE7': 6.129567 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 4,
            'latitudeE7': 49.598263 * 10000000,
            'longitudeE7': 6.130897 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 5,
            'latitudeE7': 49.598263 * 10000000,
            'longitudeE7': 6.131852 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 6,
            'latitudeE7': 49.598541 * 10000000,
            'longitudeE7': 6.133000 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 7,
            'latitudeE7': 49.598541 * 10000000,
            'longitudeE7': 6.133000 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 8,
            'latitudeE7': 49.598541 * 10000000,
            'longitudeE7': 6.133000 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 9,
            'latitudeE7': 49.598541 * 10000000,
            'longitudeE7': 6.133000 * 10000000,
        }
    ]

    fake_location_3 = [
        {
            'timestampMs': 0,
            'latitudeE7': 49.598542 * 10000000,
            'longitudeE7': 6.133002 * 10000000,
        },
        {
            'timestampMs': timestamp_scale,
            'latitudeE7': 49.598542 * 10000000,
            'longitudeE7': 6.133002 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 2,
            'latitudeE7': 49.598542 * 10000000,
            'longitudeE7': 6.133002 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 3 + 2000,
            'latitudeE7': 49.598542 * 10000000,
            'longitudeE7': 6.133002 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 4,
            'latitudeE7': 49.598542 * 10000000,
            'longitudeE7': 6.133002 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 5 + 130000,
            'latitudeE7': 49.598542 * 10000000,
            'longitudeE7': 6.133002 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 6 + 10000,
            'latitudeE7': 49.598541 * 10000000,
            'longitudeE7': 6.133000 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 7 + 10000,
            'latitudeE7': 49.598541 * 10000000,
            'longitudeE7': 6.133000 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 8 + 10000,
            'latitudeE7': 49.598541 * 10000000,
            'longitudeE7': 6.133000 * 10000000,
        },
        {
            'timestampMs': timestamp_scale * 9 + 10000,
            'latitudeE7': 49.598541 * 10000000,
            'longitudeE7': 6.133000 * 10000000,
        }
    ]

    return [fake_location_1, fake_location_2, fake_location_3]
