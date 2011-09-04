from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_is_repetition_free_sequence_01():

    assert sequencetools.is_repetition_free_sequence(range(6))


def test_sequencetools_is_repetition_free_sequence_02():

    assert not sequencetools.is_repetition_free_sequence([0, 1, 2, 2, 4, 5])


def test_sequencetools_is_repetition_free_sequence_03():
    '''True when expr is an empty sequence.'''

    assert sequencetools.is_repetition_free_sequence([])


def test_sequencetools_is_repetition_free_sequence_04():
    '''False when expr is not a sequence.'''

    assert not sequencetools.is_repetition_free_sequence(17)
