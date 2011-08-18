from abjad import *
import copy


def test_Rest___copy___01():
    '''Copy rest.
    '''

    rest_1 = Rest((1, 4))
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert rest_1.format == rest_2.format
    assert rest_1 is not rest_2


def test_Rest___copy___02():
    '''Copy rest with LilyPond multiplier.
    '''

    rest_1 = Rest((1, 4), (1, 2))
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert rest_1.format == rest_2.format
    assert rest_1 is not rest_2


def test_Rest___copy___03():
    '''Copy rest with LilyPond grob overrides and LilyPond context settings.
    '''

    rest_1 = Rest((1, 4))
    rest_1.override.staff.note_head.color = 'red'
    rest_1.override.accidental.color = 'red'
    rest_1.set.tuplet_full_length = True
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, Rest)
    assert isinstance(rest_2, Rest)
    assert rest_1.format == rest_2.format
    assert rest_1 is not rest_2
