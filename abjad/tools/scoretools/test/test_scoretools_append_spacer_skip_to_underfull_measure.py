# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_append_spacer_skip_to_underfull_measure_01():
    r'''Handles measure prolation from time signature
    non-power-of-two denominator.
    '''

    measure = Measure((4, 12), "c'8 d'8 e'8 f'8")
    measure.implicit_scaling = True
    detach(TimeSignature, measure)
    time_signature = TimeSignature((5, 12))
    attach(time_signature, measure)
    assert measure.is_underfull

    scoretools.append_spacer_skip_to_underfull_measure(measure)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 5/12
            \scaleDurations #'(2 . 3) {
                c'8
                d'8
                e'8
                f'8
                s1 * 1/8
            }
        }
        '''
        )

    assert inspect_(measure).is_well_formed()


def test_scoretools_append_spacer_skip_to_underfull_measure_02():
    r'''Handles regular measure with no time signature prolation.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    detach(TimeSignature, measure)
    time_signature = TimeSignature((5, 8))
    attach(time_signature, measure)
    assert measure.is_underfull

    scoretools.append_spacer_skip_to_underfull_measure(measure)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 5/8
            c'8
            d'8
            e'8
            f'8
            s1 * 1/8
        }
        '''
        )

    assert inspect_(measure).is_well_formed()
