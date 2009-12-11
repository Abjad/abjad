from abjad import *


def test_listtools_repeat_n_cycles_01( ):

   g = listtools._generator(1, 6)
   t = list(listtools.repeat_n_cycles(g, 3))
   assert t == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]


def test_listtools_repeat_n_cycles_02( ):
   '''Yield nothing n is zero.'''

   g = listtools._generator(1, 6)
   t = list(listtools.repeat_n_cycles(g, 0))
   assert t == [ ]
