from abjad import *


def test_listtools_sequence_to_degree_of_rotational_symmetry_01( ):
  
   assert listtools.sequence_to_degree_of_rotational_symmetry([1, 1, 1, 1, 1, 1]) == 1
   assert listtools.sequence_to_degree_of_rotational_symmetry([1, 2, 1, 2, 1, 2]) == 2
   assert listtools.sequence_to_degree_of_rotational_symmetry([1, 2, 1, 1, 2, 1]) == 3
   assert listtools.sequence_to_degree_of_rotational_symmetry([1, 2, 1, 1, 1, 1]) == 6


def test_listtools_sequence_to_degree_of_rotational_symmetry_02( ):
   '''Empty iterable boundary case.'''

   assert listtools.sequence_to_degree_of_rotational_symmetry([ ]) is None
