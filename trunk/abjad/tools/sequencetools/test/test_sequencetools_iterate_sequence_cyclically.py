# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_iterate_sequence_cyclically_01():
    r'''Defaults step to 1 and start to 0.
    '''

    sequence_1 = [1, 2, 3, 4, 5, 6, 7]
    sequence_2 = list(sequencetools.iterate_sequence_cyclically(sequence_1, length=20))

    assert sequence_2 == [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6]


def test_sequencetools_iterate_sequence_cyclically_02():
    r'''Step can be greater than 1.
    '''

    sequence_1 = [1, 2, 3, 4, 5, 6, 7]
    step = list(sequencetools.iterate_sequence_cyclically(sequence_1, 2, length=20))

    assert step == [1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4]


def test_sequencetools_iterate_sequence_cyclically_03():
    r'''Start can be greater than 0.
    '''

    sequence_1 = [1, 2, 3, 4, 5, 6, 7]
    sequence_2 = list(sequencetools.iterate_sequence_cyclically(sequence_1, 2, 3, length=20))

    assert sequence_2 == [4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7]


def test_sequencetools_iterate_sequence_cyclically_04():
    r'''Step can be negative.
    '''

    sequence_1 = [1, 2, 3, 4, 5, 6, 7]
    step = list(sequencetools.iterate_sequence_cyclically(sequence_1, -2, 5, length=20))

    assert step == [6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3]


def test_sequencetools_iterate_sequence_cyclically_05():
    r'''Works on generator input.
    '''

    sequence_2 = list(sequencetools.iterate_sequence_cyclically(xrange(1, 8), length=20))
    assert sequence_2 == [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6]

    sequence_2 = list(sequencetools.iterate_sequence_cyclically(xrange(1, 8), 2, length=20))
    assert sequence_2 == [1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4]

    sequence_2 = list(sequencetools.iterate_sequence_cyclically(xrange(1, 8), 2, 3, length=20))
    assert sequence_2 == [4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7]

    sequence_2 = list(sequencetools.iterate_sequence_cyclically(xrange(1, 8), step=-2, start=5, length=20))
    assert sequence_2 == [6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3]
