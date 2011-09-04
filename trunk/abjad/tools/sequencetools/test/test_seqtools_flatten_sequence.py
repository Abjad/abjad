from abjad import *
from abjad.tools import sequencetools
import py.test


def test_sequencetools_flatten_sequence_01():
    l = [1, 2, 3, 4, 5]
    new = sequencetools.flatten_sequence(l)
    assert new == [1, 2, 3, 4, 5]


def test_sequencetools_flatten_sequence_02():
    l = [(1, 2), [3, 4]]
    new = sequencetools.flatten_sequence(l)
    assert new == [1, 2, 3, 4]


def test_sequencetools_flatten_sequence_03():
    l = [(1, 2), [3, (4, 5)]]
    new = sequencetools.flatten_sequence(l)
    assert new == [1, 2, 3, 4, 5]


def test_sequencetools_flatten_sequence_04():
    l = [(1, 2), [3, (4, 5)]]
    new = sequencetools.flatten_sequence(l, klasses = (list, ))
    assert new == [(1, 2), 3, (4, 5)]


def test_sequencetools_flatten_sequence_05():
    l = [(1, 2), [3, (4, 5)]]
    assert py.test.raises(AssertionError, 'sequencetools.flatten_sequence(l, klasses = (tuple, ))')


def test_sequencetools_flatten_sequence_06():
    l = [1, [2, 3, [4]], 5, [6, 7, [8]]]
    assert sequencetools.flatten_sequence(l, depth = 0) == [1, [2, 3, [4]], 5, [6, 7, [8]]]
    assert sequencetools.flatten_sequence(l, depth = 1) == [1, 2, 3, [4], 5, 6, 7, [8]]
    assert sequencetools.flatten_sequence(l, depth = 2) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert sequencetools.flatten_sequence(l, depth = 2) == sequencetools.flatten_sequence(l, depth = 99)
