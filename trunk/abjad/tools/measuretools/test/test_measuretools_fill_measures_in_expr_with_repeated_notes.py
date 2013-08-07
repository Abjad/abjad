# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_fill_measures_in_expr_with_repeated_notes_01():
    r'''Populate non-power-of-two measure with note train.
    '''

    measure = Measure((5, 18), [])
    measuretools.fill_measures_in_expr_with_repeated_notes(measure, Duration(1, 16))

    r'''
    {
        \time 5/18
        \scaleDurations #'(8 . 9) {
            c'16
            c'16
            c'16
            c'16
            c'16
        }
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure.lilypond_format,
        r'''
        {
            \time 5/18
            \scaleDurations #'(8 . 9) {
                c'16
                c'16
                c'16
                c'16
                c'16
            }
        }
        '''
        )
