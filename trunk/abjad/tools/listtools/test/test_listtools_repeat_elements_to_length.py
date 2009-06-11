from abjad import *
import py.test


def test_listtools_repeat_elements_to_length_01( ):

   l = [1, 1, 2, 3, 5, 5, 6]
   t = listtools.repeat_elements_to_length(l, 2)

   assert t == [1, 1, 1, 1, 2, 2, 3, 3, 5, 5, 5, 5, 6, 6]


def test_listtools_repeat_elements_to_length_02( ):

   l = [1, -1, 2, -3, 5, -5, 6]
   t = listtools.repeat_elements_to_length(l, 2)

   assert t == [1, 1, -1, -1, 2, 2, -3, -3, 5, 5, -5, -5, 6, 6]


def test_listtools_repeat_elements_to_length_03( ):

   assert py.test.raises(
      TypeError, "listtools.repeat_elements_to_length('foo')")
