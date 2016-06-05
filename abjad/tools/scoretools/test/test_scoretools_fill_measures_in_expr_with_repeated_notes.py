# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_fill_measures_in_expr_with_repeated_notes_01():
    r'''Populates non-power-of-two measure with repeated notes.
    '''

    measure = Measure((5, 18), [])
    measure.implicit_scaling = True
    scoretools.fill_measures_in_expr_with_repeated_notes(measure, Duration(1, 16))

    assert format(measure) == stringtools.normalize(
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

    assert inspect_(measure).is_well_formed()
