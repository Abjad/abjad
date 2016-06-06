# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_scale_measure_denominator_and_adjust_measure_contents_01():
    r'''Makes measure with power-of-two denominator into equivalent
    measure with non-power-of-two denominator.
    Assignable 3/2 multiplier conserves note heads.
    '''

    measure = Measure((2, 8), "c'8 d'8")
    beam = Beam()
    attach(beam, measure[:])

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 2/8
            c'8 [
            d'8 ]
        }
        '''
        )

    scoretools.scale_measure_denominator_and_adjust_measure_contents(
        measure, 3)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 3/12
            \scaleDurations #'(2 . 3) {
                c'8. [
                d'8. ]
            }
        }
        '''
        )

    assert inspect_(measure).is_well_formed()


def test_scoretools_scale_measure_denominator_and_adjust_measure_contents_02():
    r'''Make measure with power-of-two denominator into equivalent
    measure with non-power-of-two denominator.
    Nonassignable 5/4 multiplier induces ties.
    '''

    measure = Measure((2, 8), "c'8 d'8")
    beam = Beam()
    attach(beam, measure[:])

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 2/8
            c'8 [
            d'8 ]
        }
        '''
        )

    scoretools.scale_measure_denominator_and_adjust_measure_contents(
        measure, 5)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 5/20
            \scaleDurations #'(4 . 5) {
                c'8 ~ [
                c'32
                d'8 ~
                d'32 ]
            }
        }
        '''
        )

    assert inspect_(measure).is_well_formed()


def test_scoretools_scale_measure_denominator_and_adjust_measure_contents_03():
    r'''Make measure with power-of-two denominatorinto equivalent
    measure with non-power-of-two denominator.
    Assignable 7/4 multiplier conserves note_heads.
    '''

    measure = Measure((2, 8), "c'8 d'8")
    beam = Beam()
    attach(beam, measure[:])

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 2/8
            c'8 [
            d'8 ]
        }
        '''
        )

    scoretools.scale_measure_denominator_and_adjust_measure_contents(
        measure, 7)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 7/28
            \scaleDurations #'(4 . 7) {
                c'8.. [
                d'8.. ]
            }
        }
        '''
        )

    assert inspect_(measure).is_well_formed()


def test_scoretools_scale_measure_denominator_and_adjust_measure_contents_04():
    r'''Make measure with power-of-two denominatorinto equivalent
    measure with non-power-of-two denominator.
    Nonassignable 9/8 multiplier induces ties.
    '''

    measure = Measure((2, 8), "c'8 d'8")
    beam = Beam()
    attach(beam, measure[:])

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 2/8
            c'8 [
            d'8 ]
        }
        '''
        )

    scoretools.scale_measure_denominator_and_adjust_measure_contents(
        measure, 9)

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 9/36
            \scaleDurations #'(8 . 9) {
                c'8 ~ [
                c'64
                d'8 ~
                d'64 ]
            }
        }
        '''
        )

    assert inspect_(measure).is_well_formed()
