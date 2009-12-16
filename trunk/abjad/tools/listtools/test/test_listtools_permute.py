from abjad import *


def test_listtools_permute_01( ):

   l = [10, 11, 12, 13, 14, 15]
   t = listtools.permute(l, [5, 4, 0, 1, 2, 3])

   assert t == (15, 14, 10, 11, 12, 13)


def test_listtools_permute_02( ):

   l = [10, 11, 12, 13, 14, 15]
   t = listtools.permute(l, range(6))

   assert t == (10, 11, 12, 13, 14, 15)
