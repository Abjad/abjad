from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_zip_sequences_cyclically_01():
    '''zip_cyclic can take two non-iterables.'''

    t = sequencetools.zip_sequences_cyclically(1, 2)
    assert t == [(1, 2)]


def test_sequencetools_zip_sequences_cyclically_02():
    '''zip_cyclic can take a list of length 1 and a non-iterables.'''

    t = sequencetools.zip_sequences_cyclically([1], 2)
    assert t == [(1, 2)]
    t = sequencetools.zip_sequences_cyclically(1, [2])
    assert t == [(1, 2)]


def test_sequencetools_zip_sequences_cyclically_03():
    '''zip_cyclic can take two lists of the same size.'''

    t = sequencetools.zip_sequences_cyclically([1, 2], ['a', 'b'])
    assert t == [(1, 'a'), (2, 'b')]


def test_sequencetools_zip_sequences_cyclically_04():
    '''zip_cyclic can take two lists of the different sizes.
        The list with the shortest size is cycled through.'''

    t = sequencetools.zip_sequences_cyclically([1, 2, 3], ['a', 'b'])
    assert t == [(1, 'a'), (2, 'b'), (3, 'a')]
    t = sequencetools.zip_sequences_cyclically([1, 2], ['a', 'b', 'c'])
    assert t == [(1, 'a'), (2, 'b'), (1, 'c')]


def test_sequencetools_zip_sequences_cyclically_05():
    '''Handle more than two iterables.'''

    a = [10, 11, 12]
    b = [20, 21]
    c = [30, 31, 32, 33]
    t = sequencetools.zip_sequences_cyclically(a, b, c)

    assert t == [(10, 20, 30), (11, 21, 31), (12, 20, 32), (10, 21, 33)]
