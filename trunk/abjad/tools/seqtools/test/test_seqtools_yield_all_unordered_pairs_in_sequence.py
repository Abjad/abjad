from abjad import *


def test_seqtools_yield_all_unordered_pairs_in_sequence_01( ):
   '''Handles input of length greater than 2.'''

   t = seqtools.yield_all_unordered_pairs_in_sequence([1, 2, 3, 4])
   assert t == [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]


def test_seqtools_yield_all_unordered_pairs_in_sequence_02( ):
   '''Handles input of length 2.'''

   t = seqtools.yield_all_unordered_pairs_in_sequence([1, 2]) == [(1, 2)]


def test_seqtools_yield_all_unordered_pairs_in_sequence_03( ):
   '''Handles input of length less than 2.'''

   assert seqtools.yield_all_unordered_pairs_in_sequence([1]) == [ ]
   assert seqtools.yield_all_unordered_pairs_in_sequence([ ]) == [ ]


def test_seqtools_yield_all_unordered_pairs_in_sequence_04( ):
   '''Handles set input. Note that we can't control
   the order in which the elements in set are iterated.
   So we must test result as an unordered set rather
   than an ordered list.'''

   t = set([1, 2, 3])
   result = seqtools.yield_all_unordered_pairs_in_sequence(t) 
   assert set(result) == set([(1, 2), (1, 3), (2, 3)])


def test_seqtools_yield_all_unordered_pairs_in_sequence_05( ):
   '''Handles duplicate input values.'''

   assert seqtools.yield_all_unordered_pairs_in_sequence([1, 1]) == [(1, 1)]
   assert seqtools.yield_all_unordered_pairs_in_sequence([1, 1, 1]) == [(1, 1), (1, 1), (1, 1)]
