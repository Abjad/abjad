from abjad import *
import py.test


def test_listtools_partition_elements_into_canonic_parts_01( ):

   l = range(10)
   t = listtools.partition_elements_into_canonic_parts(l)

   assert t == [(0,), (1,), (2,), (3,), (4,), (4, 1), (6,), (7,), (8,), (8, 1)]


def test_listtools_partition_elements_into_canonic_parts_02( ):

   l = range(10)
   t = listtools.partition_elements_into_canonic_parts(
      l, direction = 'little-endian')

   assert t == [(0,), (1,), (2,), (3,), (4,), (1, 4), (6,), (7,), (8,), (1, 8)]


def test_listtools_partition_elements_into_canonic_parts_03( ):
   '''Raise TypeError when l is not a list.
      Raise ValueError on noninteger elements in l.'''

   assert py.test.raises(
      TypeError, "listtools.partition_elements_into_canonic_parts('foo')")
   assert py.test.raises(ValueError, 
      'listtools.partition_elements_into_canonic_parts('
      '[Rational(1, 2), Rational(1, 2)])')
