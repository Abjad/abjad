from abjad import *


def test_listtools_remove_weighted_subrun_at_01( ):
   '''Remove weighted subrun from l at index i.'''

   t = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
   result = listtools.remove_weighted_subrun_at(t, 8, 0)

   assert result == [4, 5, 1, 2, 5, 5, 6]


def test_listtools_remove_weighted_subrun_at_02( ):
   '''Remove weighted subrun from l at index i.'''

   t = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
   result = listtools.remove_weighted_subrun_at(t, 13, 4)

   assert result == [1, 1, 2, 3, 5, 5, 6]
