# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Measure_scale_and_adjust_time_signature_01():
    r'''Scales power-of-two measure to non-power-of-two measure.
    No note head rewriting necessary.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    measure.scale_and_adjust_time_signature(Multiplier(2, 3))

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 3/12
            \scaleDurations #'(2 . 3) {
                c'8
                d'8
                e'8
            }
        }
        '''
        )

    assert inspect_(measure).is_well_formed()



def test_scoretools_Measure_scale_and_adjust_time_signature_02():
    r'''Scale non-power-of-two time signature to power-of-two.
    No note head rewriting necessary.
    '''

    measure = Measure((3, 12), "c'8 d'8 e'8")
    measure.scale_and_adjust_time_signature(Multiplier(3, 2))

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

    assert inspect_(measure).is_well_formed()


def test_scoretools_Measure_scale_and_adjust_time_signature_03():
    r'''Scale power-of-two time signature to power-of-two time signature.
    Noteheads rewrite with dots.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    measure.scale_and_adjust_time_signature(Multiplier(3, 2))

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 9/16
            c'8.
            d'8.
            e'8.
        }
        '''
        )

    assert inspect_(measure).is_well_formed()


def test_scoretools_Measure_scale_and_adjust_time_signature_04():
    r'''Scale power-of-two time signature to power-of-two time signature.
    Noteheads rewrite without dots.
    '''

    measure = Measure((9, 16), "c'8. d'8. e'8.")
    measure.scale_and_adjust_time_signature(Multiplier(2, 3))

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


def test_scoretools_Measure_scale_and_adjust_time_signature_05():
    r'''Scale power-of-two time signature to non-power-of-two time signature.
    No note head rewriting necessary.
    '''

    measure = Measure((9, 16), "c'16 d'16 e'16 f'16 g'16 a'16 b'16 c''16 d''16")
    measure.scale_and_adjust_time_signature(Multiplier(2, 3))

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 9/24
            \scaleDurations #'(2 . 3) {
                c'16
                d'16
                e'16
                f'16
                g'16
                a'16
                b'16
                c''16
                d''16
            }
        }
        '''
        )

    assert inspect_(measure).is_well_formed()


def test_scoretools_Measure_scale_and_adjust_time_signature_06():
    r'''Scale non-power-of-two time signature to power-of-two time signature.
    Noteheads rewrite with double duration.
    '''

    measure = Measure((3, 12), "c'8 d'8 e'8")
    measure.scale_and_adjust_time_signature(Multiplier(3))

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 3/4
            c'4
            d'4
            e'4
        }
        '''
        )

    assert inspect_(measure).is_well_formed()


def test_scoretools_Measure_scale_and_adjust_time_signature_07():
    r'''Scale power-of-two time signature by one half.
    Noteheads rewrite with half duration.
    Time signature rewrites with double denominator.
    '''

    measure = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measure.scale_and_adjust_time_signature(Multiplier(1, 2))

    assert inspect_(measure).is_well_formed()
    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 6/32
            c'32
            d'32
            e'32
            f'32
            g'32
            a'32
        }
        '''
        )


def test_scoretools_Measure_scale_and_adjust_time_signature_08():
    r'''Scale power-of-two time signature by one quarter.
    Noteheads rewrite with quarter duration.
    Time signature rewrites with quadruple denominator.
    '''

    measure = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measure.scale_and_adjust_time_signature(Multiplier(1, 4))

    assert inspect_(measure).is_well_formed()
    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 6/64
            c'64
            d'64
            e'64
            f'64
            g'64
            a'64
        }
        '''
        )


def test_scoretools_Measure_scale_and_adjust_time_signature_09():
    r'''Scale power-of-two time signature by two.
    Noteheads rewrite with double duration.
    Time signature rewrites with half denominator.
    '''

    measure = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measure.scale_and_adjust_time_signature(Multiplier(2))

    assert inspect_(measure).is_well_formed()
    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 6/8
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        '''
        )


def test_scoretools_Measure_scale_and_adjust_time_signature_10():
    r'''Scale power-of-two time signature by four.
    Noteheads rewrite with quadruple duration.
    Time signature rewrites with quarter denominator.
    '''

    measure = Measure((6, 16), "c'16 d'16 e'16 f'16 g'16 a'16")
    measure.scale_and_adjust_time_signature(Multiplier(4))

    assert inspect_(measure).is_well_formed()
    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 6/4
            c'4
            d'4
            e'4
            f'4
            g'4
            a'4
        }
        '''
        )
