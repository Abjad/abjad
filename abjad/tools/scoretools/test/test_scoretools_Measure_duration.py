# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Measure_duration_01():
    r'''Properly filled measure with power-of-two time signature.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")

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

    assert measure._contents_duration == Duration(3, 8)
    assert measure._preprolated_duration == Duration(3, 8)
    assert inspect_(measure).get_duration() == Duration(3, 8)


def test_scoretools_Measure_duration_02():
    r'''Properly filled measure with non-power-of-two time signature.
    '''

    measure = Measure((3, 10), "c'8 d'8 e'8")
    measure.implicit_scaling = True

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 3/10
            \scaleDurations #'(4 . 5) {
                c'8
                d'8
                e'8
            }
        }
        '''
        )

    assert measure._contents_duration == Duration(3, 8)
    assert measure._preprolated_duration == Duration(3, 10)
    assert inspect_(measure).get_duration() == Duration(3, 10)


def test_scoretools_Measure_duration_03():
    r'''Improperly filled measure with power-of-two time signature.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8 f'8")

    assert pytest.raises(OverfullContainerError, 'format(measure)')

    assert measure._contents_duration == Duration(4, 8)
    assert measure._preprolated_duration == Duration(4, 8)
    assert inspect_(measure).get_duration() == Duration(4, 8)


def test_scoretools_Measure_duration_04():
    r'''Impropely filled measure with non-power-of-two time signature.
    '''

    measure = Measure((3, 10), "c'8 d'8 e'8 f'8")
    measure.implicit_scaling = True

    assert pytest.raises(OverfullContainerError, 'format(measure)')

    assert measure._contents_duration == Duration(4, 8)
    assert measure._preprolated_duration == Duration(4, 10)
    assert inspect_(measure).get_duration() == Duration(4, 10)
