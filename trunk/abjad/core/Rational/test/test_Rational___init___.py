from abjad import *
import py.test


def test_Rational___init____01( ):
   '''Rational can take one or two integer arguments.'''
   r = Rational(1)
   r = Rational(1, 4)


def test_Rational___init____02( ):
   '''Rational can take a Rational.'''
   r = Rational(Rational(1, 4))
   assert r == Rational(1, 4)


def test_Rational___init____03( ):
   '''Rational can NOT initialize with floats.'''
   assert py.test.raises(TypeError, 'Rational(1.)')
   assert py.test.raises(TypeError, 'Rational(1./4)')
   assert py.test.raises(TypeError, 'Rational(1/4.)')


def test_Rational___init____04( ):
   #'''Rational can NOT initialize with zero arguments.'''
   #assert py.test.raises(TypeError, 'Rational( )')
   '''Rational with zero arguments initializes to zero.'''
   r = Rational( )
   assert r == Rational(0)


def test_Rational___init____05( ):
   '''Rational can NOT initialize with more than one Rational.'''
   assert py.test.raises(TypeError, 'Rational(Rational(1), Rational(2))')


def test_Rational___init____06( ):
   '''Rational can NOT initialize with 0 denominator.'''
   assert py.test.raises(ZeroDivisionError, 'Rational(12, 0)')


def test_Rational___init____07( ):
   #'''Rational can initialize from integer pair.'''
   '''Rational can NOT initialize from integer pair.'''

   #assert Rational((1, 2)) == Rational(1, 2)
   #assert Rational((-1, 2)) == Rational(-1, 2)
   #assert Rational((1, -2)) == Rational(-1, 2)
   assert py.test.raises(TypeError, 'Rational((1, 2))')
   assert py.test.raises(TypeError, 'Rational((-1, 2))')
   assert py.test.raises(TypeError, 'Rational((1, -2))')
