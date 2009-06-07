from abjad import *


def test_listtools_repeat_subruns_cyclic_01( ):

   l = range(20)
   t = listtools.repeat_subruns_cyclic(l, [(0, 2, 10)])

   assert t == [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


def test_listtools_repeat_subruns_cyclic_02( ):

   l = range(20)
   t = listtools.repeat_subruns_cyclic(l, [(0, 2, 5), (10, 2, 5)])

   assert t == [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


def test_listtools_repeat_subruns_cyclic_03( ):

   l = range(20)
   t = listtools.repeat_subruns_cyclic(l, [(18, 4, 2)])

   assert t == [0, 1, 18, 19, 0, 1, 18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


def test_listtools_repeat_subruns_cyclic_04( ):

   l = range(20)
   t = listtools.repeat_subruns_cyclic(l, [(18, 8, 2)])

   assert t == [0, 1, 2, 3, 4, 5, 18, 19, 0, 1, 2, 3, 4, 5, 18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
