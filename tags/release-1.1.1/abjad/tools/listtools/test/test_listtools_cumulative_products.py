from abjad import *
import py.test


def test_listtools_cumulative_products_01( ):
   '''Return list of the cumulative products of the elements in input.'''

   assert listtools.cumulative_products([1, 2, 3]) == [1, 2, 6]
   assert listtools.cumulative_products([10, -9, -8]) == [10, -90, 720]
   assert listtools.cumulative_products([0, 0, 0, 5]) == [0, 0, 0, 0]
   assert listtools.cumulative_products([-10, 10, -10, 10]) == \
      [-10, -100, 1000, 10000]


def test_listtools_cumulative_products_02( ):
   '''Raise TypeError when l is not a list.
      Raise ValueError when l is empty.'''

   assert py.test.raises(TypeError, "listtools.cumulative_products('foo')")
   assert py.test.raises(ValueError, 'listtools.cumulative_products([ ])')
