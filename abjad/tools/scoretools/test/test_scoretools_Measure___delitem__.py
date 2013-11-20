# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Measure___delitem___01():
    r'''Nonnegative indices work.

    Automatically update time signature.
    '''

    measure = Measure((4, 8), Note(0, (1, 8)) * 4)
    measure.automatically_adjust_time_signature = True
    del(measure[:1])

    assert inspect(measure).is_well_formed()
    assert systemtools.TestManager.compare(
        measure,
        r'''
        {
            \time 3/8
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_Measure___delitem___02():
    r'''Negative indices work.

    Automatically update time signatures.
    '''

    measure = Measure((4, 8), Note(0, (1, 8)) * 4)
    measure.automatically_adjust_time_signature = True
    del(measure[-1:])

    assert inspect(measure).is_well_formed()
    assert systemtools.TestManager.compare(
        measure,
        r'''
        {
            \time 3/8
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_Measure___delitem___03():
    r'''Denominator preservation in time signature.

    Automatically update time signature.
    '''

    measure = Measure((4, 8), Note(0, (1, 8)) * 4)
    measure.automatically_adjust_time_signature = True
    del(measure[:2])

    assert inspect(measure).is_well_formed()
    assert systemtools.TestManager.compare(
        measure,
        r'''
        {
            \time 2/8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_Measure___delitem___04():
    r'''Denominator changes from 8 to 16.

    Automatically update time signature.
    '''

    measure = Measure((4, 8), Note(0, (1, 16)) * 2 + Note(0, (1, 8)) * 3)
    measure.automatically_adjust_time_signature = True
    del(measure[:1])

    assert inspect(measure).is_well_formed()
    assert systemtools.TestManager.compare(
        measure,
        r'''
        {
            \time 7/16
            c'16
            c'8
            c'8
            c'8
        }
        '''
        )


def test_scoretools_Measure___delitem___05():
    r'''Trim non-power-of-two measure.

    Automatically update time signature.
    '''

    measure = Measure((4, 9), "c'8 d'8 e'8 f'8")
    measure.automatically_adjust_time_signature = True
    del(measure[:1])

    r'''
    {
        \time 3/9
        \scaleDurations #'(8 . 9) {
            d'8
            e'8
            f'8
        }
    }
    '''

    assert inspect(measure).is_well_formed()
    assert systemtools.TestManager.compare(
        measure,
        r'''
        {
            \time 3/9
            \scaleDurations #'(8 . 9) {
                d'8
                e'8
                f'8
            }
        }
        '''
        )


def test_scoretools_Measure___delitem___06():
    r'''Trim non-power-of-two measure, with denominator change.

    Automatically update time signature.
    '''

    measure = Measure((3, 9), "c'16 d'16 e'8 f'8")
    measure.automatically_adjust_time_signature = True

    r'''
    {
        \time 3/9
        \scaleDurations #'(8 . 9) {
            c'16
            d'16
            e'8
            f'8
        }
    }
    '''

    del(measure[:1])

    r'''
    {
        \time 5/18
        \scaleDurations #'(8 . 9) {
            d'16
            e'8
            f'8
        }
    }
    '''

    assert inspect(measure).is_well_formed()
    assert systemtools.TestManager.compare(
        measure,
        r'''
        {
            \time 5/18
            \scaleDurations #'(8 . 9) {
                d'16
                e'8
                f'8
            }
        }
        '''
        )


def test_scoretools_Measure___delitem___07():
    r'''Nonnegative indices work.

    Do NOT automatically update time signature.
    '''

    measure = Measure((4, 8), "c'8 c' c' c'")
    del(measure[:1])

    assert not inspect(measure).is_well_formed()
    assert len(measure) == 3
    assert inspect(measure).get_indicator(TimeSignature)


def test_scoretools_Measure___delitem___08():
    r'''Non-power-of-two measure.

    Do NOT automatically update time signature.
    '''

    measure = Measure((4, 9), "c'8 d' e' f'")
    del(measure[:1])

    assert not inspect(measure).is_well_formed()
    assert len(measure) == 3
    assert inspect(measure).get_indicator(TimeSignature)
