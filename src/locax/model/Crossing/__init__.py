class Crossing:

    def __init__(self, start_timestamp, persons):
        self.start_timestamp = start_timestamp
        self.persons = persons

        self.end_timestamp = None
        self.valid_spread = None
        self.is_infectious = False
        for person in self.persons:
            if person.is_infected:
                self.is_infectious = True

    def get_duration(self):
        return self.end_timestamp - self.start_timestamp

    def involves(self, person):
        for crossing_person in self.persons:
            if crossing_person.id == person.id:
                return True

        return False
