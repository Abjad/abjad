# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_extend_measures_in_expr_and_apply_full_measure_tuplets_to_contents_of_measures_01():
    r'''Tupletize one measure, supplement one note.
    '''

    measure = Measure((4, 8), notetools.make_repeated_notes(4))
    measuretools.extend_measures_in_expr_and_apply_full_measure_tuplets(
        measure, notetools.make_repeated_notes(1))

    r'''
    {
        \time 4/8
        \times 4/5 {
            c'8
            c'8
            c'8
            c'8
            c'8
        }
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 4/8
            \times 4/5 {
                c'8
                c'8
                c'8
                c'8
                c'8
            }
        }
        '''
        )


def test_measuretools_extend_measures_in_expr_and_apply_full_measure_tuplets_to_contents_of_measures_02():
    r'''Tupletize one measure, supplement one rest.
    '''

    measure = Measure((4, 8), notetools.make_repeated_notes(4))
    measuretools.extend_measures_in_expr_and_apply_full_measure_tuplets(
        measure, [Rest((1, 4))])

    r'''
    {
        \time 4/8
        \times 2/3 {
            c'8
            c'8
            c'8
            c'8
            r4
        }
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 4/8
            \times 2/3 {
                c'8
                c'8
                c'8
                c'8
                r4
            }
        }
        '''
        )
