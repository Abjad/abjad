from abjad import *
from abjad.tools import timesignaturetools


def test_timesignaturetools_is_equivalent_to_time_signature_with_power_of_two_denominator_01():
    '''True when meter has power-of-two denominator or when meter 
    has non-power-of-two denominator but si but mathematically equivalent to some 
    meter that does have a power-of-two denominator.
    '''

    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((1, 12)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((2, 12)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((3, 12)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((4, 12)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((5, 12)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((6, 12)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((7, 12)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((8, 12)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((9, 12)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((10, 12)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((11, 12)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((12, 12)))


def test_timesignaturetools_is_equivalent_to_time_signature_with_power_of_two_denominator_02():
    '''True when meter is power-of-two or when meter is non-power-of-two
    but mathematically equivalent to some meter with power-of-two denominator.
    '''

    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((1, 14)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((2, 14)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((3, 14)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((4, 14)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((5, 14)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((6, 14)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((7, 14)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((8, 14)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((9, 14)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((10, 14)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((11, 14)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((12, 14)))
    assert not timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((13, 14)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((14, 14)))


def test_timesignaturetools_is_equivalent_to_time_signature_with_power_of_two_denominator_03():
    '''True for binary meters.'''

    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((1, 8)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((2, 8)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((3, 8)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((4, 8)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((5, 8)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((6, 8)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((7, 8)))
    assert timesignaturetools.is_equivalent_to_time_signature_with_power_of_two_denominator(contexttools.TimeSignatureMark((8, 8)))
