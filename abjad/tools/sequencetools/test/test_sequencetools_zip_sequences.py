# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_zip_sequences_01():
    r'''Can take two lists of the same size.
    '''

    sequences = ([1, 2], ['a', 'b'])
    sequence_2 = sequencetools.zip_sequences(sequences, cyclic=True)
    assert sequence_2 == ((1, 'a'), (2, 'b'))


def test_sequencetools_zip_sequences_02():
    r'''Can take two lists of the different sizes.
    The list with the shortest size is cycled through.
    '''

    sequences = ([1, 2, 3], ['a', 'b'])
    result = sequencetools.zip_sequences(sequences, cyclic=True)
    assert result == ((1, 'a'), (2, 'b'), (3, 'a'))

    sequences = ([1, 2], ['a', 'b', 'c'])
    result = sequencetools.zip_sequences(sequences, cyclic=True)
    assert result == ((1, 'a'), (2, 'b'), (1, 'c'))


def test_sequencetools_zip_sequences_03():
    r'''Handles more than two iterables.
    '''

    a = [10, 11, 12]
    b = [20, 21]
    c = [30, 31, 32, 33]
    sequences = (a, b, c)
    result = sequencetools.zip_sequences(sequences, cyclic=True)

    assert result == ((10, 20, 30), (11, 21, 31), (12, 20, 32), (10, 21, 33))


def test_sequencetools_zip_sequences_04():
    r'''Zips and does not truncate to the length of the shortest list.
    '''

    sequences = ([1, 2, 3, 4], [11, 12, 13])
    result = sequencetools.zip_sequences(sequences, truncate=False)
    assert result == ((1, 11), (2, 12), (3, 13), (4,))


def test_sequencetools_zip_sequences_05():
    r'''Zips and does not truncate to the length of the shortest list.
    '''

    sequences = ([1, 2, 3], [11, 12, 13, 14])
    result = sequencetools.zip_sequences(sequences, truncate=False)
    assert result == ((1, 11), (2, 12), (3, 13), (14,))
