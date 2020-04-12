import json
import os

from locax.model.Person import Person


person_id_counter = 0


def load_persons():
    root_dir = './locationData/'

    sub_directories = [f for f in os.listdir(root_dir) if 'Person' in f]

    persons = []

    for sub_directory in sub_directories:
        location_history_json_path = 'Location History/Location History.json'
        target_path = os.path.join(
            './locationData', sub_directory, location_history_json_path)
        persons.append(_load_person(target_path))

    return persons


def _load_person(target_path):
    global person_id_counter
    person_id_counter += 1

    name = os.path.basename(target_path)
    name = name.replace('.json', '')

    with open(target_path, 'r') as handle:
        locations = json.load(handle)['locations']

        return Person(person_id_counter, name, locations)


if __name__ == '__main__':
    print(load_persons())
