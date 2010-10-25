from abjad import *


def test_mathtools_is_nonnegative_integer_power_of_two_01( ):
   '''Return True when expr is an integer or Fraction power of two, 
      otherwise False.'''

   assert mathtools.is_nonnegative_integer_power_of_two(0)
   assert mathtools.is_nonnegative_integer_power_of_two(1)
   assert mathtools.is_nonnegative_integer_power_of_two(2)
   assert not mathtools.is_nonnegative_integer_power_of_two(3)
   assert mathtools.is_nonnegative_integer_power_of_two(4)
   assert not mathtools.is_nonnegative_integer_power_of_two(5)
   assert not mathtools.is_nonnegative_integer_power_of_two(6)
   assert not mathtools.is_nonnegative_integer_power_of_two(7)
   assert mathtools.is_nonnegative_integer_power_of_two(8)
   assert not mathtools.is_nonnegative_integer_power_of_two(9)
   assert not mathtools.is_nonnegative_integer_power_of_two(10)
   assert not mathtools.is_nonnegative_integer_power_of_two(11)
   assert not mathtools.is_nonnegative_integer_power_of_two(12)


def test_mathtools_is_nonnegative_integer_power_of_two_02( ):
   '''Return True when expr is an integer or Fraction power of two, 
      otherwise False.'''

   assert mathtools.is_nonnegative_integer_power_of_two(0)
   assert not mathtools.is_nonnegative_integer_power_of_two(-1)
   assert not mathtools.is_nonnegative_integer_power_of_two(-2)
   assert not mathtools.is_nonnegative_integer_power_of_two(-3)
   assert not mathtools.is_nonnegative_integer_power_of_two(-4)
   assert not mathtools.is_nonnegative_integer_power_of_two(-5)
   assert not mathtools.is_nonnegative_integer_power_of_two(-6)
   assert not mathtools.is_nonnegative_integer_power_of_two(-7)
   assert not mathtools.is_nonnegative_integer_power_of_two(-8)
   assert not mathtools.is_nonnegative_integer_power_of_two(-9)
   assert not mathtools.is_nonnegative_integer_power_of_two(-10)
   assert not mathtools.is_nonnegative_integer_power_of_two(-11)
   assert not mathtools.is_nonnegative_integer_power_of_two(-12)


def test_mathtools_is_nonnegative_integer_power_of_two_03( ):
   '''Return True when expr is an integer or Fraction power of two, 
      otherwise False.'''

   assert mathtools.is_nonnegative_integer_power_of_two(Fraction(0))
   assert mathtools.is_nonnegative_integer_power_of_two(Fraction(1))
   assert mathtools.is_nonnegative_integer_power_of_two(Fraction(2))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(3))
   assert mathtools.is_nonnegative_integer_power_of_two(Fraction(4))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(5))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(6))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(7))
   assert mathtools.is_nonnegative_integer_power_of_two(Fraction(8))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(9))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(10))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(11))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(12))
   

def test_mathtools_is_nonnegative_integer_power_of_two_04( ):
   '''Return True when expr is an integer or Fraction power of two, 
      otherwise False.'''

   assert mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 1))
   assert mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 2))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 3))
   assert mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 4))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 5))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 6))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 7))
   assert mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 8))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 9))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 10))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 11))
   assert not mathtools.is_nonnegative_integer_power_of_two(Fraction(1, 12))
