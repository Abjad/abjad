from abjad import *
from abjad.tools import metertools


def test_metertools_duration_and_possible_denominators_to_meter_01( ):
    '''Find only feasible denominator in denominators list.'''

    t = metertools.duration_and_possible_denominators_to_meter(Duration(3, 2), [5, 6, 7, 8, 9])
    assert t == contexttools.TimeSignatureMark(9, 6)


def test_metertools_duration_and_possible_denominators_to_meter_02( ):
    '''Use least feasible denominator in denominators list.'''

    t = metertools.duration_and_possible_denominators_to_meter(Duration(3, 2), [4, 8, 16, 32])
    assert t == contexttools.TimeSignatureMark(6, 4)


def test_metertools_duration_and_possible_denominators_to_meter_03( ):
    '''Make meter literally from duration.'''

    t = metertools.duration_and_possible_denominators_to_meter(Duration(3, 2))
    assert t == contexttools.TimeSignatureMark(3, 2)


def test_metertools_duration_and_possible_denominators_to_meter_04( ):
    '''Make meter literally from duration
        because no feasible denomiantors in denominators list.'''

    t = metertools.duration_and_possible_denominators_to_meter(Duration(3, 2), [7, 11, 13, 19])
    assert t == contexttools.TimeSignatureMark(3, 2)


