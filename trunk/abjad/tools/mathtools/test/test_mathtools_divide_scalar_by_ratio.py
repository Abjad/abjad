from abjad import *
import py.test


def test_mathtools_divide_scalar_by_ratio_01( ):
   '''Can take integers.'''

   t = mathtools.divide_scalar_by_ratio(1, [1, 1, 2])

   assert len(t) == 3
   assert t[0] == 1 / 4.
   assert t[1] == 1 / 4.
   assert t[2] == 1 / 2.


def test_mathtools_divide_scalar_by_ratio_02( ):
   '''Can take rationals.'''

   t = mathtools.divide_scalar_by_ratio(Rational(1, 2), [1, 1, 2])

   assert len(t) == 3
   assert t[0] == Rational(1, 8)
   assert t[1] == Rational(1, 8)
   assert t[2] == Rational(1, 4)


def test_mathtools_divide_scalar_by_ratio_03( ):
   '''Raise TypeError on nonnumeric n.'''

   assert py.test.raises(
      TypeError, "mathtools.divide_scalar_by_ratio('foo', [1, 1, 3])")
