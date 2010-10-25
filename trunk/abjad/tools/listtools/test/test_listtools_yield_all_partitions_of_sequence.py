from abjad import *


def test_listtools_yield_all_partitions_of_sequence_01( ):

   assert list(listtools.yield_all_partitions_of_sequence([0, 1, 2])) == [
      [[0, 1, 2]], 
      [[0, 1], [2]], 
      [[0], [1, 2]], 
      [[0], [1], [2]]
      ]


def test_listtools_yield_all_partitions_of_sequence_02( ):

   assert list(listtools.yield_all_partitions_of_sequence([0, 1, 2, 3])) == [
      [[0, 1, 2, 3]],
      [[0, 1, 2], [3]],
      [[0, 1], [2, 3]],
      [[0, 1], [2], [3]],
      [[0], [1, 2, 3]],
      [[0], [1, 2], [3]],
      [[0], [1], [2, 3]],
      [[0], [1], [2], [3]],
   ]
