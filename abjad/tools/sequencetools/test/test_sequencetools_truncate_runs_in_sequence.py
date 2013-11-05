# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_sequencetools_truncate_runs_in_sequence_01():
    r'''Truncate subruns to length 1.
    '''

    sequence_1 = [1, 1, 2, 3, 3, 3, 9, 4, 4, 4]
    sequence_2 = sequencetools.truncate_runs_in_sequence(sequence_1)

    assert sequence_2 == [1, 2, 3, 9, 4]


def test_sequencetools_truncate_runs_in_sequence_02():
    r'''Truncate subruns to length 1.
    '''

    sequence_1 = []
    sequence_2 = sequencetools.truncate_runs_in_sequence(sequence_1)

    assert sequence_2 == []


def test_sequencetools_truncate_runs_in_sequence_03():
    r'''Raise TypeError when l is not a list.
    '''

    assert py.test.raises(TypeError, 'sequencetools.truncate_runs_in_sequence(1)')
