from abjad import *


def test_listtools_nwise_strict_01( ):

   t = list(listtools.nwise_strict(range(10), 3))
   assert t == [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), 
      (4, 5, 6), (5, 6, 7), (6, 7, 8), (7, 8, 9)]


def test_listtools_nwise_strict_02( ):
   '''Empty iterable boundary case.'''

   t = list(listtools.nwise_strict([ ], 3))
   assert t == [ ]


def test_listtools_nwise_strict_03( ):
   '''Length-1 boundary case.'''

   t = list(listtools.nwise_strict(range(10), 1))
   assert t == [(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)]
