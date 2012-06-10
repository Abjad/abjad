from experimental import specificationtools


def test_PartIndicator___init___01():
    '''Init from ratio and integer.
    '''

    part_indicator = specificationtools.PartIndicator((1, 2, 1), 0)
    assert isinstance(part_indicator, specificationtools.PartIndicator)


def test_PartIndicator___init___02():
    '''Init from other part indicator.
    '''

    part_indicator_1 = specificationtools.PartIndicator((1, 2, 1), 0)
    part_indicator_2 = specificationtools.PartIndicator(part_indicator_1)

    assert isinstance(part_indicator_1, specificationtools.PartIndicator)
    assert isinstance(part_indicator_2, specificationtools.PartIndicator)
    assert part_indicator_1 is not part_indicator_2
    assert part_indicator_1 == part_indicator_2
