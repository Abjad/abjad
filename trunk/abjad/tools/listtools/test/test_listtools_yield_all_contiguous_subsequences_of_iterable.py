from abjad import *


def test_listtools_yield_all_contiguous_subsequences_of_iterable_01( ):
   
   l = range(10)
   sublists = list(listtools.yield_all_contiguous_subsequences_of_iterable(l, 4, 5))

   assert len(sublists) == 13
   assert sublists[0] == [0, 1, 2, 3]
   assert sublists[1] == [0, 1, 2, 3, 4]
   assert sublists[2] == [1, 2, 3, 4]
   assert sublists[3] == [1, 2, 3, 4, 5]
   assert sublists[4] == [2, 3, 4, 5]
   assert sublists[5] == [2, 3, 4, 5, 6]
   assert sublists[6] == [3, 4, 5, 6]
   assert sublists[7] == [3, 4, 5, 6, 7]
   assert sublists[8] == [4, 5, 6, 7]
   assert sublists[9] == [4, 5, 6, 7, 8]
   assert sublists[10] == [5, 6, 7, 8]
   assert sublists[11] == [5, 6, 7, 8, 9]
   assert sublists[12] == [6, 7, 8, 9]
