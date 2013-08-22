# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_append_spacer_skip_to_underfull_measure_01():
    r'''Handles measure prolation from time signature non-power-of-two denominator.
    '''

    measure = Measure((4, 12), "c'8 d'8 e'8 f'8")
    inspect(measure).get_mark(contexttools.TimeSignatureMark).detach()
    contexttools.TimeSignatureMark((5, 12))(measure)
    assert measure.is_underfull

    measuretools.append_spacer_skip_to_underfull_measure(measure)

    assert testtools.compare(
        measure,
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

    assert inspect(measure).is_well_formed()


def test_measuretools_append_spacer_skip_to_underfull_measure_02():
    r'''Handles regular measure with no time signature prolation.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    inspect(measure).get_mark(contexttools.TimeSignatureMark).detach()
    contexttools.TimeSignatureMark((5, 8))(measure)
    assert measure.is_underfull

    measuretools.append_spacer_skip_to_underfull_measure(measure)

    assert testtools.compare(
        measure,
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

    assert inspect(measure).is_well_formed()
