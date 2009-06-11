from abjad import *
import py.test


def test_listtools_true_indices_01( ):

   l = [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1]
   t = listtools.true_indices(l)
   assert t == [3, 4, 5, 9, 10, 11]

   l = [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
   t = listtools.true_indices(l)
   assert t == [3, 4, 10, 14, 17, 21]


def test_listtools_true_indices_02( ):

   l = [0, 0, 0, 0, 0, 0]
   t = listtools.true_indices(l)

   assert t == [ ]


def test_listtools_true_indices_03( ):

   assert py.test.raises(TypeError, "listtools.true_indices('foo')")
