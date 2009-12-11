from abjad import *


def test_listtools_remove_elements_at_indices_cyclic_01( ):

   t = list(listtools.remove_elements_at_indices_cyclic(range(20), [0, 1], 5))
   assert t == [2, 3, 4, 7, 8, 9, 12, 13, 14, 17, 18, 19]


def test_listtools_remove_elements_at_indices_cyclic_02( ):

   t = list(listtools.remove_elements_at_indices_cyclic(
      range(20), [0, 1], 5, 1))
   assert t == [0, 3, 4, 5, 8, 9, 10, 13, 14, 15, 18, 19]


def test_listtools_remove_elements_at_indices_cyclic_03( ):

   t = list(listtools.remove_elements_at_indices_cyclic(range(20), [ ], 5))
   assert t == range(20)


def test_listtools_remove_elements_at_indices_cyclic_04( ):

   t = list(listtools.remove_elements_at_indices_cyclic(
      range(20), [-1, 99, 100], 5))
   assert t == range(20)
