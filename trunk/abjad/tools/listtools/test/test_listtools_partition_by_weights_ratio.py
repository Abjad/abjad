from abjad import *


def test_listtools_partition_by_weights_ratio_01( ):
   '''Common cases.'''

   l = [1] * 10

   result = listtools.partition_by_weights_ratio(l, [1, 1, 1])
   assert result == [[1, 1, 1], [1, 1, 1, 1], [1, 1, 1]]

   result = listtools.partition_by_weights_ratio(l, [1, 1, 1, 1])
   assert result == [[1, 1, 1], [1, 1], [1, 1, 1], [1, 1]]

   result = listtools.partition_by_weights_ratio(l, [2, 2, 3])
   assert result == [[1, 1, 1], [1, 1, 1], [1, 1, 1, 1]]

   result = listtools.partition_by_weights_ratio(l, [3, 2, 2])
   assert result == [[1, 1, 1, 1], [1, 1, 1], [1, 1, 1]]


def test_listtools_partition_by_weights_ratio_02( ):
   '''Unusual cases.'''

   l = [5, 5]

   result = listtools.partition_by_weights_ratio(l, [1, 1, 1])
   assert result == [[5], [5], []]

   result = listtools.partition_by_weights_ratio(l, [1, 1, 1, 1])
   assert result == [[5], [], [5], []]

   result = listtools.partition_by_weights_ratio(l, [2, 2, 3])
   assert result == [[5], [5], []]

   result = listtools.partition_by_weights_ratio(l, [3, 2, 2])
   assert result == [[5], [5], []]


def test_listtools_partition_by_weights_ratio_03( ):
   '''More unusual cases.'''

   l = [7, 3]

   result = listtools.partition_by_weights_ratio(l, [1, 1, 1])
   assert result == [[7], [], [3]]

   result = listtools.partition_by_weights_ratio(l, [1, 1, 1, 1])
   assert result == [[7], [], [3], []]

   result = listtools.partition_by_weights_ratio(l, [2, 2, 3])
   assert result == [[7], [], [3]]

   result = listtools.partition_by_weights_ratio(l, [3, 2, 2])
   assert result == [[7], [], [3]]
