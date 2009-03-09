from abjad import *
from abjad.helpers.is_power_of_two import _is_power_of_two


def test_is_power_of_two_01( ):
   '''Return True when expr is an integer or Rational power of two, 
      otherwise False.'''

   assert _is_power_of_two(0)
   assert _is_power_of_two(1)
   assert _is_power_of_two(2)
   assert not _is_power_of_two(3)
   assert _is_power_of_two(4)
   assert not _is_power_of_two(5)
   assert not _is_power_of_two(6)
   assert not _is_power_of_two(7)
   assert _is_power_of_two(8)
   assert not _is_power_of_two(9)
   assert not _is_power_of_two(10)
   assert not _is_power_of_two(11)
   assert not _is_power_of_two(12)


def test_is_power_of_two_02( ):
   '''Return True when expr is an integer or Rational power of two, 
      otherwise False.'''

   assert _is_power_of_two(0)
   assert not _is_power_of_two(-1)
   assert not _is_power_of_two(-2)
   assert not _is_power_of_two(-3)
   assert not _is_power_of_two(-4)
   assert not _is_power_of_two(-5)
   assert not _is_power_of_two(-6)
   assert not _is_power_of_two(-7)
   assert not _is_power_of_two(-8)
   assert not _is_power_of_two(-9)
   assert not _is_power_of_two(-10)
   assert not _is_power_of_two(-11)
   assert not _is_power_of_two(-12)


def test_is_power_of_two_03( ):
   '''Return True when expr is an integer or Rational power of two, 
      otherwise False.'''

   assert _is_power_of_two(Rational(0))
   assert _is_power_of_two(Rational(1))
   assert _is_power_of_two(Rational(2))
   assert not _is_power_of_two(Rational(3))
   assert _is_power_of_two(Rational(4))
   assert not _is_power_of_two(Rational(5))
   assert not _is_power_of_two(Rational(6))
   assert not _is_power_of_two(Rational(7))
   assert _is_power_of_two(Rational(8))
   assert not _is_power_of_two(Rational(9))
   assert not _is_power_of_two(Rational(10))
   assert not _is_power_of_two(Rational(11))
   assert not _is_power_of_two(Rational(12))
   

def test_is_power_of_two_04( ):
   '''Return True when expr is an integer or Rational power of two, 
      otherwise False.'''

   assert _is_power_of_two(Rational(1, 1))
   assert _is_power_of_two(Rational(1, 2))
   assert not _is_power_of_two(Rational(1, 3))
   assert _is_power_of_two(Rational(1, 4))
   assert not _is_power_of_two(Rational(1, 5))
   assert not _is_power_of_two(Rational(1, 6))
   assert not _is_power_of_two(Rational(1, 7))
   assert _is_power_of_two(Rational(1, 8))
   assert not _is_power_of_two(Rational(1, 9))
   assert not _is_power_of_two(Rational(1, 10))
   assert not _is_power_of_two(Rational(1, 11))
   assert not _is_power_of_two(Rational(1, 12))
