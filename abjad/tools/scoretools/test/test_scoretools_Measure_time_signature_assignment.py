# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Measure_time_signature_assignment_01():
    r'''Measures allow timesignature reassignment.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    measure.pop()
    detach(TimeSignature, measure)
    time_signature = TimeSignature((3, 8))
    attach(time_signature, measure)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 3/8
            c'8
            d'8
            e'8
        }
        '''
        )
