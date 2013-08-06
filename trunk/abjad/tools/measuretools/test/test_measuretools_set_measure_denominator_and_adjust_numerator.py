# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_set_measure_denominator_and_adjust_numerator_01():

    t = Measure((3, 8), "c'8 d'8 e'8")
    measuretools.set_measure_denominator_and_adjust_numerator(t, 16)

    r'''
    {
        \time 6/16
        c'8
        d'8
        e'8
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        {
            \time 6/16
            c'8
            d'8
            e'8
        }
        '''
        )

    measuretools.set_measure_denominator_and_adjust_numerator(t, 8)

    r'''
    {
        \time 3/8
        c'8
        d'8
        e'8
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        {
            \time 3/8
            c'8
            d'8
            e'8
        }
        '''
        )
