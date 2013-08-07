# -*- encoding: utf-8 -*-
from abjad import *


def test_timesignaturetools_duration_and_possible_denominators_to_time_signature_01():
    r'''Find only feasible denominator in denominators list.
    '''

    duration = timesignaturetools.duration_and_possible_denominators_to_time_signature(
        Duration(3, 2), [5, 6, 7, 8, 9])
    assert duration == contexttools.TimeSignatureMark((9, 6))


def test_timesignaturetools_duration_and_possible_denominators_to_time_signature_02():
    r'''Use least feasible denominator in denominators list.
    '''

    duration = timesignaturetools.duration_and_possible_denominators_to_time_signature(
        Duration(3, 2), [4, 8, 16, 32])
    assert duration == contexttools.TimeSignatureMark((6, 4))


def test_timesignaturetools_duration_and_possible_denominators_to_time_signature_03():
    r'''Make time signature literally from duration.
    '''

    duration = timesignaturetools.duration_and_possible_denominators_to_time_signature(
        Duration(3, 2))
    assert duration == contexttools.TimeSignatureMark((3, 2))


def test_timesignaturetools_duration_and_possible_denominators_to_time_signature_04():
    r'''Make time signature literally from duration
    because no feasible denomiantors in denominators list.
    '''

    t = timesignaturetools.duration_and_possible_denominators_to_time_signature(
        Duration(3, 2), [7, 11, 13, 19])
    assert t == contexttools.TimeSignatureMark((3, 2))
