from abjad import *
import py.test


def test_listtools_negate_elements_at_indices_absolutely_01( ):

   l = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
   t = listtools.negate_elements_at_indices_absolutely(l, [0, 1, 2])
   
   assert t == [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]


def test_listtools_negate_elements_at_indices_absolutely_02( ):

   l = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
   t = listtools.negate_elements_at_indices_absolutely(l, [0, 1, 2], period = 5)
   
   assert t == [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]


def test_listtools_negate_elements_at_indices_absolutely_03( ):

   assert py.test.raises(TypeError,
      "listtools.negate_elements_at_indices_absolutely('foo', [0, 1, 2])")
