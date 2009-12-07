from abjad import *


def test_listtools_get_unordered_pairs_01( ):

   t = listtools.get_unordered_pairs([1, 2, 3, 4])

   assert t == [set([1, 2]), set([1, 3]), set([1, 4]), 
      set([2, 3]), set([2, 4]), set([3, 4])]


def test_listtools_get_unordered_pairs_02( ):

   t = listtools.get_unordered_pairs([1, 2])

   assert t == [set([1, 2])]


def test_listtools_get_unordered_pairs_03( ):

   assert listtools.get_unordered_pairs([1]) == [ ]
   assert listtools.get_unordered_pairs([ ]) == [ ]


def test_listtools_get_unordered_pairs_04( ):

   t = set([0, 1, 2])

   assert listtools.get_unordered_pairs(t) == [
      set([0, 1]), set([0, 2]), set([1, 2])]
