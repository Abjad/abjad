from abjad import *


def test_listtools_count_repetitions_01( ):

   assert listtools.count_repetitions([0, 1, 2, 3, 4, 5]) == 0
   assert listtools.count_repetitions([0, 0, 1, 1, 2, 2]) == 3
   assert listtools.count_repetitions([0, 0, 0, 0, 0, 0]) == 5


def test_listtools_count_repetitions_02( ):
   '''Empty list and length-1 list boundary cases.'''

   assert listtools.count_repetitions([ ]) == 0
   assert listtools.count_repetitions([1]) == 0
