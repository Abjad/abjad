from abjad import *


def test_listtools_partition_list_once_by_counts_without_overhang_01( ):

   l = range(16)
   parts = listtools.partition_list_once_by_counts_without_overhang(l, [4, 6]) 

   "[[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15]]"

   assert len(parts) == 2
   assert parts[0] == [0, 1, 2, 3]
   assert parts[1] == [4, 5, 6, 7, 8, 9]
