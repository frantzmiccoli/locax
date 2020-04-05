from locax.location_generator.LocationGeneratorContext \
    import LocationGeneratorContext
from locax.location_generator.LocationGenerator import LocationGenerator
from locax.location_generator.persist_person_data import persist_person_data

import sys


def generate_location(start_days_ago, end_days_ago, people_count):
    context = LocationGeneratorContext()

    for i in range(0, people_count):
        generator = LocationGenerator(context)
        person_data = []

        for days_ago in range(start_days_ago, end_days_ago, -1):
            day_data = generator.get_day_data(days_ago)
            person_data += day_data

        name = 'Person-' + str(i)
        persist_person_data(name, person_data)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('usage: python src/locax/location_generator/__init__.py 10 3 40')
        sys.exit(1)

    _, start_days_ago, end_days_ago, people_count = sys.argv

    generate_location(
        int(start_days_ago),
        int(end_days_ago),
        int(people_count)
    )

