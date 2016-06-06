# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_set_measure_denominator_and_adjust_numerator_01():

    measure = Measure((3, 8), "c'8 d'8 e'8")
    scoretools.set_measure_denominator_and_adjust_numerator(measure, 16)

    r'''
    {
        \time 6/16
        c'8
        d'8
        e'8
    }
    '''

    assert inspect_(measure).is_well_formed()
    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 6/16
            c'8
            d'8
            e'8
        }
        '''
        )

    scoretools.set_measure_denominator_and_adjust_numerator(measure, 8)

    r'''
    {
        \time 3/8
        c'8
        d'8
        e'8
    }
    '''

    assert inspect_(measure).is_well_formed()
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
