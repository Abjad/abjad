from abjad import *
from abjad.tools import sequencetools
import py.test


def test_sequencetools_truncate_runs_in_sequence_01():
    '''Truncate subruns to length 1.'''

    t = [1, 1, 2, 3, 3, 3, 9, 4, 4, 4]
    result = sequencetools.truncate_runs_in_sequence(t)

    assert result == [1, 2, 3, 9, 4]


def test_sequencetools_truncate_runs_in_sequence_02():
    '''Truncate subruns to length 1.'''

    t = []
    result = sequencetools.truncate_runs_in_sequence(t)

    assert result == []


def test_sequencetools_truncate_runs_in_sequence_03():
    '''Raise TypeError when l is not a list.'''

    assert py.test.raises(TypeError, 'sequencetools.truncate_runs_in_sequence(1)')
