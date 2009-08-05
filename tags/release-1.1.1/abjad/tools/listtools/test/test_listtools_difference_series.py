from abjad import *


def test_listtools_difference_series_01( ):
   '''Return generator of differences l_i+1 - l_i for l_i in list l.'''

   t = [1, 1, 2, 3, 5, 5, 6]
   d = listtools.difference_series(t)
   assert list(d) == [0, 1, 1, 2, 0, 1]
