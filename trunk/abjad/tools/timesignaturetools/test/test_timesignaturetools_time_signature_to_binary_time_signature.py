from abjad import *
from abjad.tools import timesignaturetools


def test_timesignaturetools_time_signature_to_binary_time_signature_01():
    '''Make n/12 meters into n/8 meters, where possible.
    '''

    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((1, 12))) == contexttools.TimeSignatureMark((1, 12))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((2, 12))) == contexttools.TimeSignatureMark((2, 12))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((3, 12))) == contexttools.TimeSignatureMark((2, 8))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((4, 12))) == contexttools.TimeSignatureMark((4, 12))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((5, 12))) == contexttools.TimeSignatureMark((5, 12))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((6, 12))) == contexttools.TimeSignatureMark((4, 8))


def test_timesignaturetools_time_signature_to_binary_time_signature_02():
    '''Make n/14 meters into n/8 meters, where possible.
    '''

    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((1, 14))) == contexttools.TimeSignatureMark((1, 14))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((2, 14))) == contexttools.TimeSignatureMark((2, 14))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((3, 14))) == contexttools.TimeSignatureMark((3, 14))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((4, 14))) == contexttools.TimeSignatureMark((4, 14))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((5, 14))) == contexttools.TimeSignatureMark((5, 14))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((6, 14))) == contexttools.TimeSignatureMark((6, 14))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((7, 14))) == contexttools.TimeSignatureMark((4, 8))


def test_timesignaturetools_time_signature_to_binary_time_signature_03():
    '''Make n/24 meters into n/16 meters, where possible.
    '''

    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((1, 24))) == contexttools.TimeSignatureMark((1, 24))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((2, 24))) == contexttools.TimeSignatureMark((2, 24))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((3, 24))) == contexttools.TimeSignatureMark((2, 16))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((4, 24))) == contexttools.TimeSignatureMark((4, 24))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((5, 24))) == contexttools.TimeSignatureMark((5, 24))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((6, 24))) == contexttools.TimeSignatureMark((4, 16))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((7, 24))) == contexttools.TimeSignatureMark((7, 24))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((8, 24))) == contexttools.TimeSignatureMark((8, 24))


def test_timesignaturetools_time_signature_to_binary_time_signature_04():
    '''Make n/24 meters into n/8 meters, where possible.
    '''

    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((1, 24)), Duration(99)) == contexttools.TimeSignatureMark((1, 24))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((2, 24)), Duration(99)) == contexttools.TimeSignatureMark((2, 24))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((3, 24)), Duration(99)) == contexttools.TimeSignatureMark((1, 8))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((4, 24)), Duration(99)) == contexttools.TimeSignatureMark((4, 24))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((5, 24)), Duration(99)) == contexttools.TimeSignatureMark((5, 24))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((6, 24)), Duration(99)) == contexttools.TimeSignatureMark((2, 8))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((7, 24)), Duration(99)) == contexttools.TimeSignatureMark((7, 24))
    assert timesignaturetools.time_signature_to_binary_time_signature(contexttools.TimeSignatureMark((8, 24)), Duration(99)) == contexttools.TimeSignatureMark((8, 24))
