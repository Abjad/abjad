from abjad import *


def test_seqtools_sequence_to_degree_of_rotational_symmetry_01( ):

   assert seqtools.sequence_to_degree_of_rotational_symmetry([1, 2, 3, 4, 5, 6]) == 1
   assert seqtools.sequence_to_degree_of_rotational_symmetry([1, 2, 3, 1, 2, 3]) == 2
   assert seqtools.sequence_to_degree_of_rotational_symmetry([1, 2, 1, 2, 1, 2]) == 3
   assert seqtools.sequence_to_degree_of_rotational_symmetry([1, 1, 1, 1, 1, 1]) == 6
