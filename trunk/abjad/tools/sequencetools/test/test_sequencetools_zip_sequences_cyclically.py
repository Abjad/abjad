# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_zip_sequences_cyclically_01():
    r'''zip_cyclic can take two non-iterables.
    '''

    sequence_2 = sequencetools.zip_sequences_cyclically(1, 2)
    assert sequence_2 == [(1, 2)]


def test_sequencetools_zip_sequences_cyclically_02():
    r'''zip_cyclic can take a list of length 1 and a non-iterables.
    '''

    sequence_2 = sequencetools.zip_sequences_cyclically([1], 2)
    assert sequence_2 == [(1, 2)]
    sequence_2 = sequencetools.zip_sequences_cyclically(1, [2])
    assert sequence_2 == [(1, 2)]


def test_sequencetools_zip_sequences_cyclically_03():
    r'''zip_cyclic can take two lists of the same size.
    '''

    sequence_2 = sequencetools.zip_sequences_cyclically([1, 2], ['a', 'b'])
    assert sequence_2 == [(1, 'a'), (2, 'b')]


def test_sequencetools_zip_sequences_cyclically_04():
    r'''zip_cyclic can take two lists of the different sizes.
        The list with the shortest size is cycled through.'''

    the = sequencetools.zip_sequences_cyclically([1, 2, 3], ['a', 'b'])
    assert the == [(1, 'a'), (2, 'b'), (3, 'a')]
    the = sequencetools.zip_sequences_cyclically([1, 2], ['a', 'b', 'c'])
    assert the == [(1, 'a'), (2, 'b'), (1, 'c')]


def test_sequencetools_zip_sequences_cyclically_05():
    r'''Handle more than two iterables.
    '''

    a = [10, 11, 12]
    b = [20, 21]
    c = [30, 31, 32, 33]
    sequence_2 = sequencetools.zip_sequences_cyclically(a, b, c)

    assert sequence_2 == [(10, 20, 30), (11, 21, 31), (12, 20, 32), (10, 21, 33)]
