from abjad import *


def test_listtools_rotate_iterable_01( ):

   t = range(10)
   new = listtools.rotate_iterable(t, -3)
   assert new == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

   new = listtools.rotate_iterable(t, 4)
   assert new == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
