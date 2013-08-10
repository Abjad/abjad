# -*- encoding: utf-8 -*-
from abjad import *


def test_FixedDurationTuplet___init___01():
    r'''Initialize typical fixed-duration tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3)

    assert repr(tuplet) == "FixedDurationTuplet(1/4, [c'8, c'8, c'8])"
    assert str(tuplet) == "{@ 3:2 c'8, c'8, c'8 @}"
    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        '''
        )
    assert len(tuplet) == 3
    assert tuplet.target_duration == Fraction(1, 4)
    assert tuplet.multiplier == Fraction(2, 3)
    assert more(tuplet).get_duration() == Fraction(1, 4)


def test_FixedDurationTuplet___init___02():
    r'''Initialize empty fixed-duration tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), [])

    assert repr(tuplet) == 'FixedDurationTuplet(1/4, [])'
    assert str(tuplet) == '{@ 1/4 @}'
    assert len(tuplet) == 0
    assert tuplet.target_duration == Fraction(1, 4)
    assert tuplet.multiplier == None
    assert more(tuplet).get_duration() == Fraction(1, 4)
