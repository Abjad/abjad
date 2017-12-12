import abjad


def test_scoretools_VerticalMoment___init___01():
    r'''Initializes vertical moment from empty input.
    '''

    vertical_moment = abjad.VerticalMoment()

    assert repr(vertical_moment) == 'VerticalMoment()'
