from abjad import *


def test_listtools_partition_by_lengths_01( ):
   '''Partition list into sublists of specified counts.'''

   l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

   t = listtools.partition_by_lengths(l, [3])
   assert t == [[0, 1, 2]]

   t = listtools.partition_by_lengths(l, [3], cyclic = True) 
   assert t == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

   t = listtools.partition_by_lengths(l, [3], overhang = True)
   assert t == [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]

   t = listtools.partition_by_lengths(l, [3], cyclic = True, overhang = True)
   assert t == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]


def test_listtools_partition_by_lengths_02( ):
   '''Partition list into sublists of specified counts.'''

   l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

   t = listtools.partition_by_lengths(l, [4, 3])
   assert t == [[0, 1, 2, 3], [4, 5, 6]]

   t = listtools.partition_by_lengths(l, [4, 3], cyclic = True)
   assert t == [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13]]

   t = listtools.partition_by_lengths(l, [4, 3], overhang = True)
   assert t == [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12, 13, 14, 15]]

   t = listtools.partition_by_lengths(l, [4, 3], cyclic = True, overhang = True)
   assert t == [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13], [14, 15]]
