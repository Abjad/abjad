# -*- encoding: utf-8 -*-
from abjad import *


def test_FreeTupletSelection_fix_01():
    r'''Halve note durations.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'4 d'4 e'4")
    assert not tuplet.multiplier.is_proper_tuplet_multiplier

    r'''
    \times 1/3 {
        c'4
        d'4
        e'4
    }
    '''

    tuplets = selectiontools.select_tuplets([tuplet])
    tuplets.fix()

    r'''
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    assert select(tuplet).is_well_formed()
    assert tuplet.multiplier.is_proper_tuplet_multiplier
    assert testtools.compare(
        tuplet.lilypond_format,
        r'''
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        '''
        )


def test_FreeTupletSelection_fix_02():
    r'''Double note duration.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'32 d'32 e'32")
    assert not tuplet.multiplier.is_proper_tuplet_multiplier

    r'''
    \times 8/3 {
        c'32
        d'32
        e'32
    }
    '''

    tuplets = selectiontools.select_tuplets([tuplet])
    tuplets.fix()

    r'''
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 4/3 {
        c'16
        d'16
        e'16
    }
    '''

    assert select(tuplet).is_well_formed()
    assert tuplet.multiplier.is_proper_tuplet_multiplier
    assert testtools.compare(
        tuplet.lilypond_format,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 4/3 {
            c'16
            d'16
            e'16
        }
        '''
        )


def test_FreeTupletSelection_fix_03():
    r'''Halve note durations.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(5, 16), "c'4 d'4 e'4")
    assert not t.multiplier.is_proper_tuplet_multiplier

    r'''
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 5/12 {
        c'4
        d'4
        e'4
    }
    '''

    tuplets = selectiontools.select_tuplets([t])
    tuplets.fix()

    r'''
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 5/6 {
        c'8
        d'8
        e'8
    }
    '''

    assert select(t).is_well_formed()
    assert t.multiplier.is_proper_tuplet_multiplier
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 5/6 {
            c'8
            d'8
            e'8
        }
        '''
        )
