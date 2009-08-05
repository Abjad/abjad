from abjad import *
import py.test


def test_rational_init_01( ):
   '''Rational can take one or two integer arguments.'''
   r = Rational(1)
   r = Rational(1, 4)


def test_rational_init_02( ):
   '''Rational can take a Rational.'''
   r = Rational(Rational(1, 4))
   assert r == Rational(1, 4)


def test_rational_init_03( ):
   '''Rational can NOT initialize with floats.'''
   assert py.test.raises(AssertionError, 'Rational(1.)')
   assert py.test.raises(AssertionError, 'Rational(1./4)')
   assert py.test.raises(AssertionError, 'Rational(1/4.)')


def test_rational_init_04( ):
   '''Rational can NOT initialize with zero arguments.'''
   assert py.test.raises(TypeError, 'Rational( )')


def test_rational_init_05( ):
   '''Rational can NOT initialize with more than one Rational.'''
   assert py.test.raises(AssertionError, 'Rational(Rational(1), Rational(2))')

def test_rational_init_06( ):
   '''Rational can NOT initialize with 0 denominator.'''
   assert py.test.raises(ZeroDivisionError, 'Rational(12, 0)')
