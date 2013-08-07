# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_scale_contents_of_measures_in_expr_01():
    r'''Quadruple time signature with power-of-two denominator.
    Time siganture denominator adjusts appropriately.
    '''

    measure = Measure((3, 32), "c'32 d'32 e'32")
    spannertools.BeamSpanner(measure[:])

    measuretools.scale_contents_of_measures_in_expr(measure, Duration(4))

    r'''
    {
        \time 3/8
        c'8 [
        d'8
        e'8 ]
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure.lilypond_format,
        r'''
        {
            \time 3/8
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )


def test_measuretools_scale_contents_of_measures_in_expr_02():
    r'''Triple time signature with power-of-two denominator.
    '''

    measure = Measure((3, 32), "c'32 d'32 e'32")
    spannertools.BeamSpanner(measure[:])

    measuretools.scale_contents_of_measures_in_expr(measure, Duration(3))

    r'''
    {
        \time 9/32
        c'16. [
        d'16.
        e'16. ]
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure.lilypond_format,
        r'''
        {
            \time 9/32
            c'16. [
            d'16.
            e'16. ]
        }
        '''
        )


def test_measuretools_scale_contents_of_measures_in_expr_03():
    r'''Multiply measure with power-of-two time signature denomiantor by 2/3.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(measure[:])

    measuretools.scale_contents_of_measures_in_expr(measure, Duration(2, 3))

    r'''
    {
        \time 3/12
        \scaleDurations #'(2 . 3) {
            c'8 [
            d'8
            e'8 ]
        }
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure.lilypond_format,
        r'''
        {
            \time 3/12
            \scaleDurations #'(2 . 3) {
                c'8 [
                d'8
                e'8 ]
            }
        }
        '''
        )
