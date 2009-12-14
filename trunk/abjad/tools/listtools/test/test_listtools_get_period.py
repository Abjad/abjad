from abjad import *


def test_listtools_get_period_01( ):
  
   assert listtools.get_period([1, 1, 1, 1, 1, 1]) == 1
   assert listtools.get_period([1, 2, 1, 2, 1, 2]) == 2
   assert listtools.get_period([1, 2, 1, 1, 2, 1]) == 3
   assert listtools.get_period([1, 2, 1, 1, 1, 1]) == 6


def test_listtools_get_period_02( ):
   '''Empty iterable boundary case.'''

   assert listtools.get_period([ ]) is None
