from abjad import *
import py.test


def test_mathtools_partition_integer_into_halves_01( ):
   assert mathtools.partition_integer_into_halves(
      7, bigger = 'left') == (4, 3)
   assert mathtools.partition_integer_into_halves(
      7, bigger = 'right') == (3, 4)


def test_mathtools_partition_integer_into_halves_02( ):
   assert mathtools.partition_integer_into_halves(
      8, bigger = 'left') == (4, 4)
   assert mathtools.partition_integer_into_halves(
      8, bigger = 'right') == (4, 4)
   assert mathtools.partition_integer_into_halves(
      8, bigger = 'left', even = 'disallowed') == (5, 3)
   assert mathtools.partition_integer_into_halves(
      8, bigger = 'right', even = 'disallowed') == (3, 5)


def test_mathtools_partition_integer_into_halves_03( ):
   '''Raise TypeError on noninteger n.
      Raise ValueError on nonpositive n.'''

   assert py.test.raises(
      TypeError, "mathtools.partition_integer_into_halves('foo')")
   assert py.test.raises(
      ValueError, 'mathtools.partition_integer_into_halves(-1)')
