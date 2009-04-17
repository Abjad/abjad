from abjad import *


def test_listtools_increase_cyclic_01( ):
   l = range(10)
   listtools.increase_cyclic(l, [2, 0])
   assert l == [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]


def test_listtools_increase_cyclic_02( ):
   l = range(10)
   listtools.increase_cyclic(l, [10, -10])
   assert l == [10, 1, 12, 1, 14, 1, 16, 1, 18, 1]


def test_listtools_increase_cyclic_03( ):
   l = range(10)
   listtools.increase_cyclic(l, [10, -10], shield = False)
   assert l == [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]
