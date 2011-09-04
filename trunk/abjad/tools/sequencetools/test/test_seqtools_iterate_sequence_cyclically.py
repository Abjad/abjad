from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_iterate_sequence_cyclically_01():
    '''Defaults step to 1 and start to 0.'''

    l = [1, 2, 3, 4, 5, 6, 7]
    t = list(sequencetools.iterate_sequence_cyclically(l, length = 20))

    assert t == [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6]


def test_sequencetools_iterate_sequence_cyclically_02():
    '''Step can be greater than 1.'''

    l = [1, 2, 3, 4, 5, 6, 7]
    t = list(sequencetools.iterate_sequence_cyclically(l, 2, length = 20))

    assert t == [1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4]


def test_sequencetools_iterate_sequence_cyclically_03():
    '''Start can be greater than 0.'''

    l = [1, 2, 3, 4, 5, 6, 7]
    t = list(sequencetools.iterate_sequence_cyclically(l, 2, 3, length = 20))

    assert t == [4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7]


def test_sequencetools_iterate_sequence_cyclically_04():
    '''Step can be negative.'''

    l = [1, 2, 3, 4, 5, 6, 7]
    t = list(sequencetools.iterate_sequence_cyclically(l, -2, 5, length = 20))

    assert t == [6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3]


def test_sequencetools_iterate_sequence_cyclically_05():
    '''Works on generator input.'''

    t = list(sequencetools.iterate_sequence_cyclically(xrange(1, 8), length = 20))
    assert t == [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6]

    t = list(sequencetools.iterate_sequence_cyclically(xrange(1, 8), 2, length = 20))
    assert t == [1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4]

    t = list(sequencetools.iterate_sequence_cyclically(xrange(1, 8), 2, 3, length = 20))
    assert t == [4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7]

    t = list(sequencetools.iterate_sequence_cyclically(xrange(1, 8), step = -2, start = 5, length = 20))
    assert t == [6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3]
