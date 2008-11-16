from abjad import *
from py.test import raises

def test_rational_initialization_01( ):
   '''Rational can take one or two integer arguments.'''
   r = Rational(1)
   r = Rational(1, 4)

def test_rational_initialization_02( ):
   '''Rational can take a Rational.'''
   r = Rational(Rational(1, 4))
   assert r == Rational(1, 4)

def test_rational_initialization_03( ):
   '''Rational can NOT initialize with floats.'''
   assert raises(AssertionError, 'Rational(1.)')
   assert raises(AssertionError, 'Rational(1./4)')
   assert raises(AssertionError, 'Rational(1/4.)')

def test_rational_initialization_04( ):
   '''Rational can NOT initialize with zero arguments.'''
   assert raises(TypeError, 'Rational( )')

def test_rational_initialization_05( ):
   '''Rational can NOT initialize with more than one Rational.'''
   assert raises(AssertionError, 'Rational(Rational(1), Rational(2))')


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


