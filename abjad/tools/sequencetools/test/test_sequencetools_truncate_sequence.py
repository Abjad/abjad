# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_sequencetools_truncate_sequence_01():
    r'''truncate_to_sum can take a list.
    '''

    sequence_2 = sequencetools.truncate_sequence([2, 2, 2], 0)

    assert sequence_2 == []
    assert isinstance(sequence_2, list)


def test_sequencetools_truncate_sequence_02():
    r'''Raise TypeError when l is not a list.
    '''

    statement = "sequencetools.truncate_sequence('foo')"
    assert pytest.raises(TypeError, statement)


def test_sequencetools_truncate_sequence_03():
    r'''truncate_to_sum does work :-).
    '''

    ls = [2, 2, 1]

    sequence_2 = sequencetools.truncate_sequence(ls, 1)
    assert sequence_2 == [1]
    sequence_2 = sequencetools.truncate_sequence(ls, 2)
    assert sequence_2 == [2]
    sequence_2 = sequencetools.truncate_sequence(ls, 3)
    assert sequence_2 == [2, 1]
    sequence_2 = sequencetools.truncate_sequence(ls, 4)
    assert sequence_2 == [2, 2]
    sequence_2 = sequencetools.truncate_sequence(ls, 5)
    assert sequence_2 == [2, 2, 1]
    sequence_2 = sequencetools.truncate_sequence(ls, 6)
    assert sequence_2 == [2, 2, 1]


def test_sequencetools_truncate_sequence_04():
    r'''Raise ValueError on negative total.
    '''

    statement = 'sequence_2 = sequencetools.truncate_sequence([2, 2, 2], -1)'
    assert pytest.raises(ValueError, statement)
