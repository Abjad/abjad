# -*- encoding: utf-8 -*-
from abjad import *


def test_tuplettools_Tuplet__fix_01():
    r'''Halve note durations.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'4 d'4 e'4")
    assert not tuplet.multiplier.is_proper_tuplet_multiplier

    assert testtools.compare(
        tuplet,
        r'''
        \times 1/3 {
            c'4
            d'4
            e'4
        }
        '''
        )

    tuplet._fix()

    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        '''
        )

    assert tuplet.multiplier.is_proper_tuplet_multiplier
    assert inspect(tuplet).is_well_formed()


def test_tuplettools_Tuplet__fix_02():
    r'''Double note duration.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'32 d'32 e'32")
    assert not tuplet.multiplier.is_proper_tuplet_multiplier

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 8/3 {
            c'32
            d'32
            e'32
        }
        '''
        )

    tuplet._fix()

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 4/3 {
            c'16
            d'16
            e'16
        }
        '''
        )

    assert tuplet.multiplier.is_proper_tuplet_multiplier
    assert inspect(tuplet).is_well_formed()


def test_tuplettools_Tuplet__fix_03():
    r'''Halve note durations.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(5, 16), "c'4 d'4 e'4")
    assert not tuplet.multiplier.is_proper_tuplet_multiplier

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 5/12 {
            c'4
            d'4
            e'4
        }
        '''
        )

    tuplet._fix()

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 5/6 {
            c'8
            d'8
            e'8
        }
        '''
        )

    assert tuplet.multiplier.is_proper_tuplet_multiplier
    assert inspect(tuplet).is_well_formed()
