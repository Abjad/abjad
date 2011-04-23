from abjad import *


def test_mathtools_is_nonnegative_integer_equivalent_number_01( ):

   assert mathtools.is_nonnegative_integer_equivalent_number(0)
   assert mathtools.is_nonnegative_integer_equivalent_number(0.0)
   assert mathtools.is_nonnegative_integer_equivalent_number(Fraction(0))
   assert mathtools.is_nonnegative_integer_equivalent_number(2)
   assert mathtools.is_nonnegative_integer_equivalent_number(2.0)
   assert mathtools.is_nonnegative_integer_equivalent_number(Fraction(4, 2))


def test_mathtools_is_nonnegative_integer_equivalent_number_02( ):

   assert not mathtools.is_nonnegative_integer_equivalent_number(-1)
   assert not mathtools.is_nonnegative_integer_equivalent_number(-1.0)
   assert not mathtools.is_nonnegative_integer_equivalent_number(Fraction(-1))
