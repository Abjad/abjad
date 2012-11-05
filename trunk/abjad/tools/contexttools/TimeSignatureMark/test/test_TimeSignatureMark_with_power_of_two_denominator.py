from abjad import *


def test_TimeSignatureMark_with_power_of_two_denominator_01():
    '''Make n/12 time_signatures into n/8 time_signatures, where possible.
    '''

    assert contexttools.TimeSignatureMark((1, 12)).with_power_of_two_denominator() == (1, 12)
    assert contexttools.TimeSignatureMark((2, 12)).with_power_of_two_denominator() == (2, 12)
    assert contexttools.TimeSignatureMark((3, 12)).with_power_of_two_denominator() == (2, 8)
    assert contexttools.TimeSignatureMark((4, 12)).with_power_of_two_denominator() == (4, 12)
    assert contexttools.TimeSignatureMark((5, 12)).with_power_of_two_denominator() == (5, 12)
    assert contexttools.TimeSignatureMark((6, 12)).with_power_of_two_denominator() == (4, 8)


def test_TimeSignatureMark_with_power_of_two_denominator_02():
    '''Make n/14 time_signatures into n/8 time_signatures, where possible.
    '''

    assert contexttools.TimeSignatureMark((1, 14)).with_power_of_two_denominator() == (1, 14)
    assert contexttools.TimeSignatureMark((2, 14)).with_power_of_two_denominator() == (2, 14)
    assert contexttools.TimeSignatureMark((3, 14)).with_power_of_two_denominator() == (3, 14)
    assert contexttools.TimeSignatureMark((4, 14)).with_power_of_two_denominator() == (4, 14)
    assert contexttools.TimeSignatureMark((5, 14)).with_power_of_two_denominator() == (5, 14)
    assert contexttools.TimeSignatureMark((6, 14)).with_power_of_two_denominator() == (6, 14)
    assert contexttools.TimeSignatureMark((7, 14)).with_power_of_two_denominator() == (4, 8)


def test_TimeSignatureMark_with_power_of_two_denominator_03():
    '''Make n/24 time_signatures into n/16 time_signatures, where possible.
    '''

    assert contexttools.TimeSignatureMark((1, 24)).with_power_of_two_denominator() == (1, 24)
    assert contexttools.TimeSignatureMark((2, 24)).with_power_of_two_denominator() == (2, 24)
    assert contexttools.TimeSignatureMark((3, 24)).with_power_of_two_denominator() == (2, 16)
    assert contexttools.TimeSignatureMark((4, 24)).with_power_of_two_denominator() == (4, 24)
    assert contexttools.TimeSignatureMark((5, 24)).with_power_of_two_denominator() == (5, 24)
    assert contexttools.TimeSignatureMark((6, 24)).with_power_of_two_denominator() == (4, 16)
    assert contexttools.TimeSignatureMark((7, 24)).with_power_of_two_denominator() == (7, 24)
    assert contexttools.TimeSignatureMark((8, 24)).with_power_of_two_denominator() == (8, 24)


def test_TimeSignatureMark_with_power_of_two_denominator_04():
    '''Make n/24 time_signatures into n/8 time_signatures, where possible.
    '''

    assert contexttools.TimeSignatureMark((1, 24)).with_power_of_two_denominator(Multiplier(99)) == (1, 24)
    assert contexttools.TimeSignatureMark((2, 24)).with_power_of_two_denominator(Multiplier(99)) == (2, 24)
    assert contexttools.TimeSignatureMark((3, 24)).with_power_of_two_denominator(Multiplier(99)) == (1, 8)
    assert contexttools.TimeSignatureMark((4, 24)).with_power_of_two_denominator(Multiplier(99)) == (4, 24)
    assert contexttools.TimeSignatureMark((5, 24)).with_power_of_two_denominator(Multiplier(99)) == (5, 24)
    assert contexttools.TimeSignatureMark((6, 24)).with_power_of_two_denominator(Multiplier(99)) == (2, 8)
    assert contexttools.TimeSignatureMark((7, 24)).with_power_of_two_denominator(Multiplier(99)) == (7, 24)
    assert contexttools.TimeSignatureMark((8, 24)).with_power_of_two_denominator(Multiplier(99)) == (8, 24)
