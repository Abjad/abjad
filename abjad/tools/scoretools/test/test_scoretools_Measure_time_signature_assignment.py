# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Measure_time_signature_assignment_01():
    r'''Measures allow timesignature reassignment.
    '''

    measure = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")
    measure.pop()
    abjad.detach(abjad.TimeSignature, measure)
    time_signature = abjad.TimeSignature((3, 8))
    abjad.attach(time_signature, measure)

    assert format(measure) == abjad.String.normalize(
        r'''
        {
            \time 3/8
            c'8
            d'8
            e'8
        }
        '''
        )
