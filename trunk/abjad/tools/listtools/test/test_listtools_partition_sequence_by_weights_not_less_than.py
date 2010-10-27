from abjad import *


def test_listtools_partition_sequence_by_weights_not_less_than_01( ):
   
   l = range(10)

   result = listtools.partition_sequence_by_weights_not_less_than(l, [3])
   assert result == [[0, 1, 2]]

   result = listtools.partition_sequence_by_weights_not_less_than(l, [10])
   assert result == [[0, 1, 2, 3, 4]]

   result = listtools.partition_sequence_by_weights_not_less_than(l, [3], cyclic = True)
   assert result == [[0, 1, 2], [3], [4], [5], [6], [7], [8], [9]]

   result = listtools.partition_sequence_by_weights_not_less_than(l, [3, 10])
   assert result == [[0, 1, 2], [3, 4, 5]]


def test_listtools_partition_sequence_by_weights_not_less_than_02( ):

   l = range(10)

   result = listtools.partition_sequence_by_weights_not_less_than(
      l, [3, 10], cyclic = True)
   assert result == [[0, 1, 2], [3, 4, 5], [6], [7, 8], [9]]

   result = listtools.partition_sequence_by_weights_not_less_than(
      l, [3], overhang = True)
   assert result == [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]

   result = listtools.partition_sequence_by_weights_not_less_than(
      l, [3, 10], overhang = True) 
   assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]

   result = listtools.partition_sequence_by_weights_not_less_than(
      l, [3, 10], cyclic = True, overhang = True)
   assert result == [[0, 1, 2], [3, 4, 5], [6], [7, 8], [9]]
