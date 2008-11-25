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


def test_rational_compare_01( ):
   '''Equality #1.'''
   r = Rational(1)
   assert r == Rational(1)
   assert r == 1
   assert r == 1.0
   assert not r == Rational(1, 4)
   assert not r == 0.25
   assert raises(TypeError, "r == 'foo'")


def test_rational_compare_02( ):
   '''Equality #2.'''
   r = Rational(1, 4)
   assert not r == Rational(1)
   assert not r == 1
   assert not r == 1.0
   assert r == Rational(1, 4)
   assert r == 0.25
   assert raises(TypeError, "r == 'foo'")


def test_rational_compare_03( ):
   '''Inequality #1.'''
   r = Rational(1)
   assert not r != Rational(1)
   assert not r != 1
   assert not r != 1.0
   assert r != Rational(1, 4)
   assert r != 0.25
   assert raises(TypeError, "r != 'foo'")


def test_rational_compare_04( ):
   '''Inequality #2.'''
   r = Rational(1, 4)
   assert r != Rational(1)
   assert r != 1
   assert r != 1.0
   assert not r != Rational(1, 4)
   assert not r != 0.25
   assert raises(TypeError, "r != 'foo'")


def test_rational_compare_05( ):
   '''Greater-than, #1.'''
   r = Rational(1)
   assert not r > Rational(1)
   assert not r > 1
   assert not r > 1.0
   assert r > Rational(1, 4)
   assert r > 0.25
   assert raises(TypeError, "r > 'foo'")


def test_rational_compare_06( ):
   '''Greater-than, #2.'''
   r = Rational(1, 4)
   assert not r > Rational(1)
   assert not r > 1
   assert not r > 1.0
   assert not r > Rational(1, 4)
   assert not r > 0.25
   assert raises(TypeError, "r > 'foo'")


def test_rational_compare_06( ):
   '''Greater-than-or-equal-to, #1.'''
   r = Rational(1)
   assert r >= Rational(1)
   assert r >= 1
   assert r >= 1.0
   assert r >= Rational(1, 4)
   assert r >= 0.25
   assert raises(TypeError, "r >= 'foo'")


def test_rational_compare_07( ):
   '''Greater-than-or-equal-to, #2.'''
   r = Rational(1, 4)
   assert not r >= Rational(1)
   assert not r >= 1
   assert not r >= 1.0
   assert r >= Rational(1, 4)
   assert r >= 0.25
   assert raises(TypeError, "r >= 'foo'")


def test_rational_compare_08( ):
   '''Less-than, #1.'''
   r = Rational(1)
   assert not r < Rational(1)
   assert not r < 1
   assert not r < 1.0
   assert not r < Rational(1, 4)
   assert not r < 0.25
   assert raises(TypeError, "r < 'foo'")


def test_rational_compare_09( ):
   '''Less-than, #2.'''
   r = Rational(1, 4)
   assert r < Rational(1)
   assert r < 1
   assert r < 1.0
   assert not r < Rational(1, 4)
   assert not r < 0.25
   assert raises(TypeError, "r < 'foo'")


def test_rational_compare_10( ):
   '''Less-than-or-equal-to, #1.'''
   r = Rational(1)
   assert r <= Rational(1)
   assert r <= 1
   assert r <= 1.0
   assert not r <= Rational(1, 4)
   assert not r <= 0.25
   assert raises(TypeError, "r <= 'foo'")


def test_rational_compare_11( ):
   '''Less-than-or-equal-to, #2.'''
   r = Rational(1, 4)
   assert r <= Rational(1)
   assert r <= 1
   assert r <= 1.0
   assert r <= Rational(1, 4)
   assert r <= 0.25
   assert raises(TypeError, "r <= 'foo'")
