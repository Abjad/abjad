# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_yield_all_unordered_pairs_of_sequence_01():
    r'''Handles input of length greater than 2.
    '''

    t = list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 2, 3, 4]))
    assert t == [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]


def test_sequencetools_yield_all_unordered_pairs_of_sequence_02():
    r'''Handles input of length 2.
    '''

    assert list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 2])) == [(1, 2)]


def test_sequencetools_yield_all_unordered_pairs_of_sequence_03():
    r'''Handles input of length less than 2.
    '''

    assert list(sequencetools.yield_all_unordered_pairs_of_sequence([1])) == []
    assert list(sequencetools.yield_all_unordered_pairs_of_sequence([])) == []


def test_sequencetools_yield_all_unordered_pairs_of_sequence_04():
    r'''Handles duplicate input values.
    '''

    assert list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 1])) == [(1, 1)]
    assert list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 1, 1])) == [(1, 1), (1, 1), (1, 1)]
