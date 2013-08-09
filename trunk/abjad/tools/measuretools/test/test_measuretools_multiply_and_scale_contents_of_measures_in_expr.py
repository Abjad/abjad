# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_multiply_and_scale_contents_of_measures_in_expr_01():
    r'''Concentrate one measure three times.
        Time signature 3/8 goes to 9/24.
        Numerator and denominator both triple.'''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(measure[:])
    measuretools.multiply_and_scale_contents_of_measures_in_expr(measure, [(3, 3)])

    r'''
    {
        \time 9/24
        \scaleDurations #'(2 . 3) {
            c'16 [
            d'16
            e'16 ]
            c'16 [
            d'16
            e'16 ]
            c'16 [
            d'16
            e'16 ]
        }
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 9/24
            \scaleDurations #'(2 . 3) {
                c'16 [
                d'16
                e'16 ]
                c'16 [
                d'16
                e'16 ]
                c'16 [
                d'16
                e'16 ]
            }
        }
        '''
        )


def test_measuretools_multiply_and_scale_contents_of_measures_in_expr_02():
    r'''Concentrate one measure four times over five.
    Time signature 3/16 goes to 12/80.
    Numerator quadruples and denominator quintuples.
    '''

    measure = Measure((3, 16), "c'16 d'16 e'16")
    spannertools.BeamSpanner(measure[:])
    measuretools.multiply_and_scale_contents_of_measures_in_expr(measure, [(4, 5)])

    r'''
    {
        \time 12/80
        \scaleDurations #'(4 . 5) {
            c'64 [
            d'64
            e'64 ]
            c'64 [
            d'64
            e'64 ]
            c'64 [
            d'64
            e'64 ]
            c'64 [
            d'64
            e'64 ]
        }
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 12/80
            \scaleDurations #'(4 . 5) {
                c'64 [
                d'64
                e'64 ]
                c'64 [
                d'64
                e'64 ]
                c'64 [
                d'64
                e'64 ]
                c'64 [
                d'64
                e'64 ]
            }
        }
        '''
        )


def test_measuretools_multiply_and_scale_contents_of_measures_in_expr_03():
    r'''Concentrate one measure four times over four.
        Time signature 3/16 goes to 12/64.
        Numerator and denominator both quadruple.'''

    measure = Measure((3, 16), "c'16 d'16 e'16")
    spannertools.BeamSpanner(measure[:])
    measuretools.multiply_and_scale_contents_of_measures_in_expr(measure, [(4, 4)])

    r'''
    {
        \time 12/64
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 12/64
            c'64 [
            d'64
            e'64 ]
            c'64 [
            d'64
            e'64 ]
            c'64 [
            d'64
            e'64 ]
            c'64 [
            d'64
            e'64 ]
        }
        '''
        )


def test_measuretools_multiply_and_scale_contents_of_measures_in_expr_04():
    r'''Concentrate one measure two times over four.
        Time signature 3/16 goes to 6/64.
        Numerator doubles and denominator quadruples.'''

    measure = Measure((3, 16), "c'16 d'16 e'16")
    spannertools.BeamSpanner(measure[:])
    measuretools.multiply_and_scale_contents_of_measures_in_expr(measure, [(2, 4)])

    r'''
    {
        \time 6/64
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
    }
    '''

    assert select(measure).is_well_formed()
    assert testtools.compare(
        measure,
        r'''
        {
            \time 6/64
            c'64 [
            d'64
            e'64 ]
            c'64 [
            d'64
            e'64 ]
        }
        '''
        )
