from abjad import *
from abjad.tools import timesignaturetools


def test_timesignaturetools_duration_and_possible_denominators_to_time_signature_01():
    '''Find only feasible denominator in denominators list.
    '''

    t = timesignaturetools.duration_and_possible_denominators_to_time_signature(Duration(3, 2), [5, 6, 7, 8, 9])
    assert t == contexttools.TimeSignatureMark((9, 6))


def test_timesignaturetools_duration_and_possible_denominators_to_time_signature_02():
    '''Use least feasible denominator in denominators list.
    '''

    t = timesignaturetools.duration_and_possible_denominators_to_time_signature(Duration(3, 2), [4, 8, 16, 32])
    assert t == contexttools.TimeSignatureMark((6, 4))


def test_timesignaturetools_duration_and_possible_denominators_to_time_signature_03():
    '''Make meter literally from duration.
    '''

    t = timesignaturetools.duration_and_possible_denominators_to_time_signature(Duration(3, 2))
    assert t == contexttools.TimeSignatureMark((3, 2))


def test_timesignaturetools_duration_and_possible_denominators_to_time_signature_04():
    '''Make meter literally from duration
    because no feasible denomiantors in denominators list.
    '''

    t = timesignaturetools.duration_and_possible_denominators_to_time_signature(Duration(3, 2), [7, 11, 13, 19])
    assert t == contexttools.TimeSignatureMark((3, 2))
