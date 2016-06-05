# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_extend_measures_in_expr_and_apply_full_measure_tuplets_to_contents_of_measures_01():
    r'''Tupletize one measure, supplement one note.
    '''

    measure = Measure((4, 8), scoretools.make_repeated_notes(4))
    scoretools.extend_measures_in_expr_and_apply_full_measure_tuplets(
        measure, scoretools.make_repeated_notes(1))

    assert format(measure) == stringtools.normalize(
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

    assert inspect_(measure).is_well_formed()


def test_scoretools_extend_measures_in_expr_and_apply_full_measure_tuplets_to_contents_of_measures_02():
    r'''Tupletize one measure, supplement one rest.
    '''

    measure = Measure((4, 8), "c'8 c'8 c'8 c'8")
    scoretools.extend_measures_in_expr_and_apply_full_measure_tuplets(
        measure, [Rest((1, 4))])

    assert format(measure) == stringtools.normalize(
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

    assert inspect_(measure).is_well_formed()
