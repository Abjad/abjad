# -*- encoding: utf-8 -*-
from abjad import *


def test_FreeTupletSelection_set_denominator_to_at_least_01():

    tuplet = Tuplet(Fraction(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplets = selectiontools.select_tuplets(tuplet)
    tuplets.set_denominator_to_at_least(8)

    r'''
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 6/10 {
        c'4
        d'8
        e'8
        f'4
        g'2
    }
    '''

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 6/10 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        '''
        )


def test_FreeTupletSelection_set_denominator_to_at_least_02():

    tuplet = Tuplet(Fraction(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplets = selectiontools.select_tuplets(tuplet)
    tuplets.set_denominator_to_at_least(16)

    r'''
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 12/20 {
        c'4
        d'8
        e'8
        f'4
        g'2
    }
    '''

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 12/20 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        '''
        )


def test_FreeTupletSelection_set_denominator_to_at_least_03():

    tuplet = Tuplet(Fraction(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplets = selectiontools.select_tuplets(tuplet)
    tuplets.set_denominator_to_at_least(2)

    r'''
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 3/5 {
        c'4
        d'8
        e'8
        f'4
        g'2
    }
    '''

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        '''
        )
