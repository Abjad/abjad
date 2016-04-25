# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Measure__duration_and_possible_denominators_to_time_signature_01():
    r'''Find only feasible denominator in denominators list.
    '''

    time_signature = \
        Measure._duration_and_possible_denominators_to_time_signature(
        Duration(3, 2),
        [5, 6, 7, 8, 9],
        )

    assert time_signature == TimeSignature((9, 6))


def test_scoretools_Measure__duration_and_possible_denominators_to_time_signature_02():
    r'''Use least feasible denominator in denominators list.
    '''

    time_signature = \
        Measure._duration_and_possible_denominators_to_time_signature(
        Duration(3, 2),
        [4, 8, 16, 32],
        )

    assert time_signature == TimeSignature((6, 4))


def test_scoretools_Measure__duration_and_possible_denominators_to_time_signature_03():
    r'''Make time signature literally from time_signature.
    '''

    time_signature = \
        Measure._duration_and_possible_denominators_to_time_signature(
        Duration(3, 2),
        )

    assert time_signature == TimeSignature((3, 2))


def test_scoretools_Measure__duration_and_possible_denominators_to_time_signature_04():
    r'''Make time signature literally from time_signature
    because no feasible denomiantors in denominators list.
    '''

    time_signature = \
        Measure._duration_and_possible_denominators_to_time_signature(
        Duration(3, 2),
        [7, 11, 13, 19],
        )

    assert time_signature == TimeSignature((3, 2))
