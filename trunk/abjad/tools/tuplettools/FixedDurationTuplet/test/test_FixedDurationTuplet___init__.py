# -*- encoding: utf-8 -*-
from abjad import *


def test_FixedDurationTuplet___init___01():
    r'''Initialize typical fixed-duration tuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3)

    assert repr(tuplet) == "FixedDurationTuplet(1/4, [c'8, c'8, c'8])"
    assert str(tuplet) == "{@ 3:2 c'8, c'8, c'8 @}"
    assert testtools.compare(
        tuplet.lilypond_format,
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
    assert tuplet.get_duration() == Fraction(1, 4)


def test_FixedDurationTuplet___init___02():
    r'''Initialize empty fixed-duration tuplet.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(1, 4), [])

    assert repr(t) == 'FixedDurationTuplet(1/4, [])'
    assert str(t) == '{@ 1/4 @}'
    assert len(t) == 0
    assert t.target_duration == Fraction(1, 4)
    assert t.multiplier == None
    assert t.get_duration() == Fraction(1, 4)
