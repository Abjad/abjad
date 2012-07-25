from experimental.interpretationtools.Division import Division


def test_Division___init___01():
    '''Initialize from other division.
    '''

    division_1 = Division((4, 8))
    division_2 = Division(division_1)

    assert not division_1 is division_2
    assert division_1 == division_2


def test_Division___init___02():
    '''Initialize from other division.
    '''

    division_1 = Division((4, 8), is_left_open=True)
    division_2 = Division(division_1)

    assert not division_1 is division_2
    assert division_1 == division_2
    assert not division_1.is_left_closed
    assert not division_2.is_left_closed
