from abjad import *
import py.test


def test_listtools_truncate_to_weight_01( ):
   '''Truncate list l such that listtools.weight(l) == total.'''

   l = [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]

   assert listtools.truncate_to_weight(l, 1) == [-1]
   assert listtools.truncate_to_weight(l, 2) == [-1, 1]
   assert listtools.truncate_to_weight(l, 3) == [-1, 2]
   assert listtools.truncate_to_weight(l, 4) == [-1, 2, -1]
   assert listtools.truncate_to_weight(l, 5) == [-1, 2, -2]
   assert listtools.truncate_to_weight(l, 6) == [-1, 2, -3]
   assert listtools.truncate_to_weight(l, 7) == [-1, 2, -3, 1]
   assert listtools.truncate_to_weight(l, 8) == [-1, 2, -3, 2]
   assert listtools.truncate_to_weight(l, 9) == [-1, 2, -3, 3]
   assert listtools.truncate_to_weight(l, 10) == [-1, 2, -3, 4]


def test_listtools_truncate_to_weight_02( ):
   '''Return empty list when total is zero.'''

   assert listtools.truncate_to_weight([1, 2, 3, 4, 5], 0) == [ ]


def test_listtools_truncate_to_weight_03( ):
   '''Raise TypeError when l is not a list.
      Raise ValueError on negative weight.'''

   assert py.test.raises(TypeError, "listtools.truncate_to_weight('foo', 1)")
   assert py.test.raises(
      ValueError, "listtools.truncate_to_weight([1, 2, 3], -1)")
