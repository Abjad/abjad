from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_get_sequence_degree_of_rotational_symmetry_01():

    assert sequencetools.get_sequence_degree_of_rotational_symmetry([1, 2, 3, 4, 5, 6]) == 1
    assert sequencetools.get_sequence_degree_of_rotational_symmetry([1, 2, 3, 1, 2, 3]) == 2
    assert sequencetools.get_sequence_degree_of_rotational_symmetry([1, 2, 1, 2, 1, 2]) == 3
    assert sequencetools.get_sequence_degree_of_rotational_symmetry([1, 1, 1, 1, 1, 1]) == 6
