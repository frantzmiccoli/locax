from locax.location_generator.persist_person_data import _get_gps_coordinates


def test_get_gps_coordinates():
    fake_point = {'x': 20, 'y': 10}
    gps_point = _get_gps_coordinates(fake_point)

    assert(abs(gps_point[0] - 49) < 2)
    assert(abs(gps_point[1] - 6) < 2)
