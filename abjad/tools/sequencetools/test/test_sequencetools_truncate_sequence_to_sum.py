# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_sequencetools_truncate_sequence_to_sum_01():
    r'''truncate_to_sum can take a list.
    '''

    sequence_2 = sequencetools.truncate_sequence_to_sum([2, 2, 2], 0)

    #assert sequence_2 == [0]
    assert sequence_2 == []
    assert isinstance(sequence_2, list)


#def test_sequencetools_truncate_sequence_to_sum_02():
#   r'''truncate_to_sum can take a tuple.'''
#   sequence_2 = sequencetools.truncate_sequence_to_sum((2, 2, 2), 0)
#   assert sequence_2 == (0, )
#   assert isinstance(sequence_2, tuple)


def test_sequencetools_truncate_sequence_to_sum_03():
    r'''Raise TypeError when l is not a list.
    '''

    assert py.test.raises(TypeError, "sequencetools.truncate_sequence_to_sum('foo')")


def test_sequencetools_truncate_sequence_to_sum_04():
    r'''truncate_to_sum does work :-).
    '''

    ls = [2, 2, 1]

    sequence_2 = sequencetools.truncate_sequence_to_sum(ls, 1)
    assert sequence_2 == [1]
    sequence_2 = sequencetools.truncate_sequence_to_sum(ls, 2)
    assert sequence_2 == [2]
    sequence_2 = sequencetools.truncate_sequence_to_sum(ls, 3)
    assert sequence_2 == [2, 1]
    sequence_2 = sequencetools.truncate_sequence_to_sum(ls, 4)
    assert sequence_2 == [2, 2]
    sequence_2 = sequencetools.truncate_sequence_to_sum(ls, 5)
    assert sequence_2 == [2, 2, 1]
    sequence_2 = sequencetools.truncate_sequence_to_sum(ls, 6)
    assert sequence_2 == [2, 2, 1]


# ERRORS #

def test_sequencetools_truncate_sequence_to_sum_05():
    r'''Raise ValueError on negative total.
    '''

    assert py.test.raises(ValueError,
        'sequence_2 = sequencetools.truncate_sequence_to_sum([2, 2, 2], -1)')
