# -*- encoding: utf-8 -*-
from abjad import *


def test_FixedDurationTuplet_01():
    r'''Nest typical fdtuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), [
        tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3),
        Note(0, (1, 8)),
        Note(0, (1, 8)),
        Note(0, (1, 8))])
    assert repr(tuplet) == "FixedDurationTuplet(1/2, [{@ 3:2 c'8, c'8, c'8 @}, c'8, c'8, c'8])"
    assert str(tuplet) == "{@ 5:4 {@ 3:2 c'8, c'8, c'8 @}, c'8, c'8, c'8 @}"
    assert tuplet.target_duration == Fraction(1, 2)
    assert tuplet.multiplier == Fraction(4, 5)
    assert inspect(tuplet).get_duration() == Fraction(1, 2)
    assert repr(tuplet[0]) == "FixedDurationTuplet(1/4, [c'8, c'8, c'8])"
    assert str(tuplet[0]) == "{@ 3:2 c'8, c'8, c'8 @}"
    assert len(tuplet[0]) == 3
    assert tuplet[0].target_duration == Fraction(1, 4)
    assert tuplet[0].multiplier == Fraction(2, 3)
    assert inspect(tuplet[0]).get_duration() == Fraction(1, 5)


def test_FixedDurationTuplet_02():
    r'''Nest empty fdtuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), [
        tuplettools.FixedDurationTuplet(Duration(2, 8), []),
        Note(0, (1, 8)),
        Note(0, (1, 8)),
        Note(0, (1, 8))])
    assert repr(tuplet) == "FixedDurationTuplet(1/2, [{@ 1/4 @}, c'8, c'8, c'8])"
    assert str(tuplet) == "{@ 5:4 {@ 1/4 @}, c'8, c'8, c'8 @}"
    assert tuplet.target_duration == Fraction(1, 2)
    assert tuplet.multiplier == Fraction(4, 5)
    assert inspect(tuplet).get_duration() == Fraction(1, 2)
    assert repr(tuplet[0]) == 'FixedDurationTuplet(1/4, [])'
    assert str(tuplet[0]) == '{@ 1/4 @}'
    assert len(tuplet[0]) == 0
    assert tuplet[0].target_duration == Fraction(1, 4)
    assert tuplet[0].multiplier == None
    assert inspect(tuplet[0]).get_duration() == Fraction(1, 5)


def test_FixedDurationTuplet_03():
    r'''Test 1-multiplier fdtuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 2)
    assert repr(tuplet) == "FixedDurationTuplet(1/4, [c'8, c'8])"
    assert str(tuplet) == "{@ 1:1 c'8, c'8 @}"
    assert testtools.compare(
        tuplet,
        r'''
        {
            c'8
            c'8
        }
        '''
        )


def test_FixedDurationTuplet_04():
    r'''Test 1-multiplier fdtuplet.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3)
    tuplet.pop()
    assert repr(tuplet) == "FixedDurationTuplet(1/4, [c'8, c'8])"
    assert str(tuplet) == "{@ 1:1 c'8, c'8 @}"
    assert testtools.compare(
        tuplet,
        r'''
        {
            c'8
            c'8
        }
        '''
        )


def test_FixedDurationTuplet_05():
    r'''Tuplet.is_invisible formats compressed music.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    assert tuplet.is_invisible is None
    tuplet.is_invisible = True
    assert testtools.compare(
        tuplet,
        r'''
        \scaleDurations #'(2 . 3) {
            c'8
            c'8
            c'8
        }
        '''
        )

    r'''
    \scaleDurations #'(2 . 3) {
        c'8
        c'8
        c'8
    }
    '''

    tuplet.is_invisible = False
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
