from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_retain_sequence_elements_at_indices_01():

    t = sequencetools.retain_sequence_elements_at_indices(range(20), [1, 16, 17, 18])
    assert t == [1, 16, 17, 18]


def test_sequencetools_retain_sequence_elements_at_indices_02():

    t = sequencetools.retain_sequence_elements_at_indices(range(20), [])
    assert t == []


def test_sequencetools_retain_sequence_elements_at_indices_03():

    t = sequencetools.retain_sequence_elements_at_indices(range(20), [99, 100, 101])
    assert t == []
