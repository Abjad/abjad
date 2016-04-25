# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_TimeSignature_with_power_of_two_denominator_01():
    r'''Make n/12 time_signatures into n/8 time_signatures, where possible.
    '''

    assert TimeSignature((1, 12)).with_power_of_two_denominator() == (1, 12)
    assert TimeSignature((2, 12)).with_power_of_two_denominator() == (2, 12)
    assert TimeSignature((3, 12)).with_power_of_two_denominator() == (2, 8)
    assert TimeSignature((4, 12)).with_power_of_two_denominator() == (4, 12)
    assert TimeSignature((5, 12)).with_power_of_two_denominator() == (5, 12)
    assert TimeSignature((6, 12)).with_power_of_two_denominator() == (4, 8)


def test_indicatortools_TimeSignature_with_power_of_two_denominator_02():
    r'''Make n/14 time_signatures into n/8 time_signatures, where possible.
    '''

    assert TimeSignature((1, 14)).with_power_of_two_denominator() == (1, 14)
    assert TimeSignature((2, 14)).with_power_of_two_denominator() == (2, 14)
    assert TimeSignature((3, 14)).with_power_of_two_denominator() == (3, 14)
    assert TimeSignature((4, 14)).with_power_of_two_denominator() == (4, 14)
    assert TimeSignature((5, 14)).with_power_of_two_denominator() == (5, 14)
    assert TimeSignature((6, 14)).with_power_of_two_denominator() == (6, 14)
    assert TimeSignature((7, 14)).with_power_of_two_denominator() == (4, 8)


def test_indicatortools_TimeSignature_with_power_of_two_denominator_03():
    r'''Make n/24 time_signatures into n/16 time_signatures, where possible.
    '''

    assert TimeSignature((1, 24)).with_power_of_two_denominator() == (1, 24)
    assert TimeSignature((2, 24)).with_power_of_two_denominator() == (2, 24)
    assert TimeSignature((3, 24)).with_power_of_two_denominator() == (2, 16)
    assert TimeSignature((4, 24)).with_power_of_two_denominator() == (4, 24)
    assert TimeSignature((5, 24)).with_power_of_two_denominator() == (5, 24)
    assert TimeSignature((6, 24)).with_power_of_two_denominator() == (4, 16)
    assert TimeSignature((7, 24)).with_power_of_two_denominator() == (7, 24)
    assert TimeSignature((8, 24)).with_power_of_two_denominator() == (8, 24)


def test_indicatortools_TimeSignature_with_power_of_two_denominator_04():
    r'''Make n/24 time_signatures into n/8 time_signatures, where possible.
    '''

    assert TimeSignature((1, 24)).with_power_of_two_denominator(Multiplier(99)) == (1, 24)
    assert TimeSignature((2, 24)).with_power_of_two_denominator(Multiplier(99)) == (2, 24)
    assert TimeSignature((3, 24)).with_power_of_two_denominator(Multiplier(99)) == (1, 8)
    assert TimeSignature((4, 24)).with_power_of_two_denominator(Multiplier(99)) == (4, 24)
    assert TimeSignature((5, 24)).with_power_of_two_denominator(Multiplier(99)) == (5, 24)
    assert TimeSignature((6, 24)).with_power_of_two_denominator(Multiplier(99)) == (2, 8)
    assert TimeSignature((7, 24)).with_power_of_two_denominator(Multiplier(99)) == (7, 24)
    assert TimeSignature((8, 24)).with_power_of_two_denominator(Multiplier(99)) == (8, 24)
