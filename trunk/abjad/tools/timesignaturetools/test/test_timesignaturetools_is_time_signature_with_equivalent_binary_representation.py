from abjad import *
from abjad.tools import timesignaturetools


def test_timesignaturetools_is_time_signature_with_equivalent_binary_representation_01():
    '''True when meter is binary or when meter is nonbinary
    but mathematically equivalent to some binary meter.
    '''

    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((1, 12)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((2, 12)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((3, 12)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((4, 12)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((5, 12)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((6, 12)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((7, 12)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((8, 12)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((9, 12)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((10, 12)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((11, 12)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((12, 12)))


def test_timesignaturetools_is_time_signature_with_equivalent_binary_representation_02():
    '''True when meter is binary or when meter is nonbinary
        but mathematically equivalent to some binary meter.'''

    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((1, 14)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((2, 14)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((3, 14)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((4, 14)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((5, 14)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((6, 14)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((7, 14)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((8, 14)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((9, 14)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((10, 14)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((11, 14)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((12, 14)))
    assert not timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((13, 14)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((14, 14)))


def test_timesignaturetools_is_time_signature_with_equivalent_binary_representation_03():
    '''True for binary meters.'''

    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((1, 8)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((2, 8)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((3, 8)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((4, 8)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((5, 8)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((6, 8)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((7, 8)))
    assert timesignaturetools.is_time_signature_with_equivalent_binary_representation(contexttools.TimeSignatureMark((8, 8)))
