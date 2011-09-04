from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_yield_outer_product_of_sequences_01():

    t = list(sequencetools.yield_outer_product_of_sequences([[1, 2, 3], ['a', 'b']]))
    assert t == [[1, 'a'], [1, 'b'], [2, 'a'], [2, 'b'], [3, 'a'], [3, 'b']]


def test_sequencetools_yield_outer_product_of_sequences_02():

    t = list(sequencetools.yield_outer_product_of_sequences([[1, 2, 3], ['a', 'b'], ['X', 'Y']]))
    assert t == [[1, 'a', 'X'], [1, 'a', 'Y'], [1, 'b', 'X'], [1, 'b', 'Y'], [2, 'a', 'X'] , [2, 'a', 'Y'], [2, 'b', 'X'], [2, 'b', 'Y'], [3, 'a', 'X'], [3, 'a', 'Y'], [3, 'b', 'X'], [3, 'b', 'Y']]


def test_sequencetools_yield_outer_product_of_sequences_03():

    t = list(sequencetools.yield_outer_product_of_sequences([[1, 2, 3], [4, 5], [6, 7, 8]]))
    assert t == [[1, 4, 6], [1, 4, 7], [1, 4, 8], [1, 5, 6], [1, 5, 7], [1, 5, 8], [2, 4, 6], [2, 4, 7], [2, 4, 8], [2, 5, 6], [2, 5, 7], [2, 5, 8], [3, 4, 6], [3, 4, 7], [3, 4, 8], [3, 5, 6], [3, 5, 7], [3, 5, 8]]
