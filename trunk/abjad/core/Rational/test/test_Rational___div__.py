from abjad import *
import py.test


def test_Rational___div___01( ):
   '''0 / Rational'''
   r = Rational(1, 4)
   assert 0 / r == 0
   assert 0./ r == 0.
   assert Rational(0) / r == Rational(0)


def test_Rational___div___02( ):
   '''Rational / 0'''
   r = Rational(1, 4)
   assert py.test.raises(ZeroDivisionError, 'r / 0')
   assert py.test.raises(ZeroDivisionError, 'r / 0.')
   assert py.test.raises(ZeroDivisionError, 'r / Rational(0)')
