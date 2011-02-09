from abjad import *


def test_seqtools_get_degree_of_rotational_symmetry_of_sequence_01( ):

   assert seqtools.get_degree_of_rotational_symmetry_of_sequence([1, 2, 3, 4, 5, 6]) == 1
   assert seqtools.get_degree_of_rotational_symmetry_of_sequence([1, 2, 3, 1, 2, 3]) == 2
   assert seqtools.get_degree_of_rotational_symmetry_of_sequence([1, 2, 1, 2, 1, 2]) == 3
   assert seqtools.get_degree_of_rotational_symmetry_of_sequence([1, 1, 1, 1, 1, 1]) == 6
