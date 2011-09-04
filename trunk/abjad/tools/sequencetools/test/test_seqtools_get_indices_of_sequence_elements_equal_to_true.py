from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_get_indices_of_sequence_elements_equal_to_true_01():

    l = [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1]
    t = sequencetools.get_indices_of_sequence_elements_equal_to_true(l)
    assert t == (3, 4, 5, 9, 10, 11)


def test_sequencetools_get_indices_of_sequence_elements_equal_to_true_02():

    l = [0, 0, 0, 0, 0, 0]
    t = sequencetools.get_indices_of_sequence_elements_equal_to_true(l)
    assert t == ()
