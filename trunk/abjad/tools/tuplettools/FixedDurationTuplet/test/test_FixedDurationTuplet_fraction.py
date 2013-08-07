# -*- encoding: utf-8 -*-
from abjad import *


def test_FixedDurationTuplet_fraction_01():
    r'''Fraction format tuplets with non-power of two denominators.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(3, 8), "c'8 d'8 e'8 f'8")

    r'''
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 3/4 {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert select(tuplet).is_well_formed()
    assert testtools.compare(
        tuplet.lilypond_format,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )


def test_FixedDurationTuplet_fraction_02():
    r'''Fraction format all augmentations, even ones with power-of-two denominator.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(4, 8), "c'8 d'8 e'8")


    r'''
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 4/3 {
        c'8
        d'8
        e'8
    }
    '''

    assert select(tuplet).is_well_formed()
    assert testtools.compare(
        tuplet.lilypond_format,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 4/3 {
            c'8
            d'8
            e'8
        }
        '''
        )


def test_FixedDurationTuplet_fraction_03():
    r'''Do not fraction format trivial tuplets.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(3, 8), "c'8 d'8 e'8")

    r'''
    {
        c'8
        d'8
        e'8
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        {
            c'8
            d'8
            e'8
        }
        '''
        )
