# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_fill_measures_in_expr_with_full_measure_spacer_skips_01():
    r'''Populates non-power-of-two measure with time-scaled skip.
    '''

    measure = Measure((5, 18), [])
    measure.implicit_scaling = True
    scoretools.fill_measures_in_expr_with_full_measure_spacer_skips(measure)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 5/18
            \scaleDurations #'(8 . 9) {
                s1 * 5/16
            }
        }
        '''
        )

    assert inspect_(measure).is_well_formed()


def test_scoretools_fill_measures_in_expr_with_full_measure_spacer_skips_02():
    r'''Populates measures conditionally.

    Iteration control tests index of iteration.
    '''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    staff.extend("abj: | 2/8 g'8 a'8 || 2/8 b'8 c''8 |")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )

    def iterctrl(measure, i):
        return i % 2 == 1

    scoretools.fill_measures_in_expr_with_full_measure_spacer_skips(
        staff, iterctrl)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                s1 * 1/4
            }
            {
                g'8
                a'8
            }
            {
                s1 * 1/4
            }
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_scoretools_fill_measures_in_expr_with_full_measure_spacer_skips_03():
    r'''Populates measures conditionally.

    Iteration control tests measure length.
    '''

    staff = Staff([
        Measure((2, 8), "c'8 d'8"),
        Measure((3, 8), "c'8 d'8 e'8"),
        Measure((4, 8), "c'8 d'8 e'8 f'8"),
        ])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 3/8
                c'8
                d'8
                e'8
            }
            {
                \time 4/8
                c'8
                d'8
                e'8
                f'8
            }
        }
        '''
        )

    scoretools.fill_measures_in_expr_with_full_measure_spacer_skips(
        staff,
        lambda m, i: 2 < len(m),
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 3/8
                s1 * 3/8
            }
            {
                \time 4/8
                s1 * 1/2
            }
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
