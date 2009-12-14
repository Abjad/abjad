from abjad import *


def test_listtools_remove_repetitions_01( ):

   l = [0, 0, 1, 1, 2, 2, 3, 4, 5, 5]
   t = list(listtools.remove_repetitions(l))
   
   assert t == [0, 1, 2, 3, 4, 5]


def test_listtools_remove_repetitions_02( ):

   l = [0, 0, 0, 0, 0, 0, 0]
   t = list(listtools.remove_repetitions(l))
   
   assert t == [0]
   

def test_listtools_remove_repetitions_03( ):
   '''Empty list and length-1 list boundary cases.'''

   assert list(listtools.remove_repetitions([ ])) == [ ]
   assert list(listtools.remove_repetitions([99])) == [99]
