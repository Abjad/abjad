# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_yield_all_combinations_of_elements_01():

    assert list(sequencetools.yield_all_combinations_of_elements([1, 2, 3, 4])) == [
        [], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3], [4],
        [1, 4], [2, 4], [1, 2, 4], [3, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]


def test_sequencetools_yield_all_combinations_of_elements_02():

    assert list(sequencetools.yield_all_combinations_of_elements('text')) == [
        '', 't', 'e', 'te', 'x', 'tx', 'ex', 'tex',
        't', 'tt', 'et', 'tet', 'xt', 'txt', 'ext', 'text']


def test_sequencetools_yield_all_combinations_of_elements_03():
    r'''Yield all combinations of iterable at least minimum length
    and with at most maximum length.
    '''

    assert list(sequencetools.yield_all_combinations_of_elements([1, 2, 3, 4], 2, 2)) == [
        [1, 2], [1, 3], [2, 3], [1, 4], [2, 4], [3, 4]]
