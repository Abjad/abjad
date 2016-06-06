# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Tuplet_set_minimum_denominator_01():

    tuplet = Tuplet(Multiplier(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplet.set_minimum_denominator(8)

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/10 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        '''
        )

    assert inspect_(tuplet).is_well_formed()


def test_scoretools_Tuplet_set_minimum_denominator_02():

    tuplet = Tuplet(Multiplier(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplet.set_minimum_denominator(16)

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 12/20 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        '''
        )

    assert inspect_(tuplet).is_well_formed()


def test_scoretools_Tuplet_set_minimum_denominator_03():

    tuplet = Tuplet(Multiplier(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplet.set_minimum_denominator(2)

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        '''
        )

    assert inspect_(tuplet).is_well_formed()
