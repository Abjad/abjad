from abjad import *
from abjad.tools import sequencetools
import py.test


def test_sequencetools_sum_sequence_elements_at_indices_01():
    '''Sum slices cyclically at every fourth index.'''

    t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 1)], period = 4)
    assert result == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 2)], period = 4)
    assert result == [1, 2, 3, 9, 6, 7, 17, 10, 11]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 3)], period = 4)
    assert result == [3, 3, 15, 7, 27, 11]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 4)], period = 4)
    assert result == [6, 22, 38]


def test_sequencetools_sum_sequence_elements_at_indices_02():
    '''Sum slice at only the zeroth index.
        Append overhang elements.'''

    t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 1)])
    assert result == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 2)])
    assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 3)])
    assert result == [3, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 4)])
    assert result == [6, 4, 5, 6, 7, 8, 9, 10, 11]


def test_sequencetools_sum_sequence_elements_at_indices_03():
    '''Sum every 5, 6, 7 or 8 elements together.
        Do append incomplete final sums.'''

    t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 5)], period = 5, overhang = True)
    assert result == [10, 35, 21]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 6)], period = 6, overhang = True)
    assert result == [15, 51]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 7)], period = 7, overhang = True)
    assert result == [21, 45]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 8)], period = 8, overhang = True)
    assert result == [28, 38]


def test_sequencetools_sum_sequence_elements_at_indices_04():
    '''Sum every 5, 6, 7 or 8 elements together.
        Do not append incomplete final sums.'''

    t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 5)], period = 5, overhang = False)
    assert result == [10, 35]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 6)], period = 6, overhang = False)
    assert result == [15, 51]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 7)], period = 7, overhang = False)
    assert result == [21]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 8)], period = 8, overhang = False)
    assert result == [28]


def test_sequencetools_sum_sequence_elements_at_indices_05():
    '''Sum at multiple points in each period.'''

    t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    result = sequencetools.sum_sequence_elements_at_indices(t, [(0, 2), (2, 2)], period = 5)
    assert result == [1, 5, 4, 11, 15, 9, 21]


def test_sequencetools_sum_sequence_elements_at_indices_06():
    '''Affected indices must be less than period.'''

    t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    assert py.test.raises(ValueError, 'sequencetools.sum_sequence_elements_at_indices(t, [(0, 99)], period = 4)')
