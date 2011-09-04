from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_count_length_two_runs_in_sequence_01():

    assert sequencetools.count_length_two_runs_in_sequence([0, 1, 2, 3, 4, 5]) == 0
    assert sequencetools.count_length_two_runs_in_sequence([0, 0, 1, 1, 2, 2]) == 3
    assert sequencetools.count_length_two_runs_in_sequence([0, 0, 0, 0, 0, 0]) == 5


def test_sequencetools_count_length_two_runs_in_sequence_02():
    '''Empty list and length-1 list boundary cases.'''

    assert sequencetools.count_length_two_runs_in_sequence([]) == 0
    assert sequencetools.count_length_two_runs_in_sequence([1]) == 0
