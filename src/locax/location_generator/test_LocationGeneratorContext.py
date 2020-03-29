from locax.location_generator.LocationGeneratorContext \
    import LocationGeneratorContext


def test_init():
    location_generator_context = LocationGeneratorContext()

    assert(len(location_generator_context.points_of_interest) == 100)

    one_poi = location_generator_context.points_of_interest[0]
    assert(one_poi['x'] <= 100)
    assert(one_poi['x'] >= 0)
    assert(one_poi['y'] <= 100)
    assert(one_poi['y'] >= 0)
