from abjad import *
from abjad.tools import sequencetools
import py.test


def test_sequencetools_truncate_sequence_to_weight_01():
    '''Truncate list l such that mathtools.weight(l) == total.'''

    l = [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]

    assert sequencetools.truncate_sequence_to_weight(l, 1) == [-1]
    assert sequencetools.truncate_sequence_to_weight(l, 2) == [-1, 1]
    assert sequencetools.truncate_sequence_to_weight(l, 3) == [-1, 2]
    assert sequencetools.truncate_sequence_to_weight(l, 4) == [-1, 2, -1]
    assert sequencetools.truncate_sequence_to_weight(l, 5) == [-1, 2, -2]
    assert sequencetools.truncate_sequence_to_weight(l, 6) == [-1, 2, -3]
    assert sequencetools.truncate_sequence_to_weight(l, 7) == [-1, 2, -3, 1]
    assert sequencetools.truncate_sequence_to_weight(l, 8) == [-1, 2, -3, 2]
    assert sequencetools.truncate_sequence_to_weight(l, 9) == [-1, 2, -3, 3]
    assert sequencetools.truncate_sequence_to_weight(l, 10) == [-1, 2, -3, 4]


def test_sequencetools_truncate_sequence_to_weight_02():
    '''Return empty list when total is zero.'''

    assert sequencetools.truncate_sequence_to_weight([1, 2, 3, 4, 5], 0) == []


def test_sequencetools_truncate_sequence_to_weight_03():
    '''Raise TypeError when l is not a list.
        Raise ValueError on negative weight.'''

    assert py.test.raises(TypeError, "sequencetools.truncate_sequence_to_weight('foo', 1)")
    assert py.test.raises(
        ValueError, "sequencetools.truncate_sequence_to_weight([1, 2, 3], -1)")
