from abjad import *


def test_listtools_yield_all_combinations_of_sequence_01( ):

   assert list(listtools.yield_all_combinations_of_sequence([1, 2, 3, 4])) == [
      [ ], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3], [4], 
      [1, 4], [2, 4], [1, 2, 4], [3, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]


def test_listtools_yield_all_combinations_of_sequence_02( ):
   
   assert list(listtools.yield_all_combinations_of_sequence('text')) == [
      '', 't', 'e', 'te', 'x', 'tx', 'ex', 'tex', 
      't', 'tt', 'et', 'tet', 'xt', 'txt', 'ext', 'text']


def test_listtools_yield_all_combinations_of_sequence_03( ):
   '''Yield all combinations of iterable at least minimum length
   and with at most maximum length.
   '''

   assert list(listtools.yield_all_combinations_of_sequence([1, 2, 3, 4], 2, 2)) == [
      [1, 2], [1, 3], [2, 3], [1, 4], [2, 4], [3, 4]]
