from abjad import *


def test_listtools_is_decreasing_monotonically_01( ):
   '''True when the elements in l decrease monotonically.'''

   l = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
   assert listtools.is_decreasing_monotonically(l)

   l = [3, 3, 3, 3, 3, 3, 3, 2, 1, 0]
   assert listtools.is_decreasing_monotonically(l)


def test_listtools_is_decreasing_monotonically_02( ):
   '''False when the elements in l do not decrease monotonically.'''

   l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   assert not listtools.is_decreasing_monotonically(l)

   l = [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]
   assert not listtools.is_decreasing_monotonically(l)


def test_listtools_is_decreasing_monotonically_03( ):
   '''True when l is empty.'''

   l = [ ]
   assert listtools.is_decreasing_monotonically(l)
