from abjad import *
from abjad.tools import seqtools


def test_seqtools_get_sequence_degree_of_rotational_symmetry_01( ):

   assert seqtools.get_sequence_degree_of_rotational_symmetry([1, 2, 3, 4, 5, 6]) == 1
   assert seqtools.get_sequence_degree_of_rotational_symmetry([1, 2, 3, 1, 2, 3]) == 2
   assert seqtools.get_sequence_degree_of_rotational_symmetry([1, 2, 1, 2, 1, 2]) == 3
   assert seqtools.get_sequence_degree_of_rotational_symmetry([1, 1, 1, 1, 1, 1]) == 6
