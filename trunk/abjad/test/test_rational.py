from abjad import *
from py.test import raises

def test_rational_divide_01( ):
   '''0 / Rational'''
   r = Rational(1, 4)
   assert 0 / r == 0
   assert 0./ r == 0.
   assert Rational(0) / r == Rational(0)

def test_rational_divide_02( ):
   '''Rational / 0'''
   r = Rational(1, 4)
   assert raises(ZeroDivisionError, 'r / 0')
   assert raises(ZeroDivisionError, 'r / 0.')
   assert raises(ZeroDivisionError, 'r / Rational(0)')

