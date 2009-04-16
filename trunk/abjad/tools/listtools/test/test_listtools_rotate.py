from abjad import *


def test_listtools_rotate_01( ):

   t = range(10)
   new = listtools.rotate(t, 'left', 3)
   assert new == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

   new = listtools.rotate(t, 'right', 4)
   assert new == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]


def test_listtools_rotate_02( ):

   t = range(10)
   listtools.rotate(t, 'left', 3, action = 'in place')
   assert t == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

   listtools.rotate(t, 'right', 4, action = 'in place')
   assert t == [9, 0, 1, 2, 3, 4, 5, 6, 7, 8]
