from abjad import *
import py.test


def test_Rational_compare_01( ):
   '''Equality #1.'''
   r = Rational(1)
   assert     r == Rational(1)
   assert     r == 1
   assert     r == 1.0
   assert not r == Rational(1, 4)
   assert not r == 0.25
   assert not r == 'foo'


def test_Rational_compare_02( ):
   '''Equality #2.'''
   r = Rational(1, 4)
   assert not r == Rational(1)
   assert not r == 1
   assert not r == 1.0
   assert     r == Rational(1, 4)
   assert     r == 0.25
   assert not r == 'foo'


def test_Rational_compare_03( ):
   '''Inequality #1.'''
   r = Rational(1)
   assert not r != Rational(1)
   assert not r != 1
   assert not r != 1.0
   assert     r != Rational(1, 4)
   assert     r != 0.25
   assert     r != 'foo'


def test_Rational_compare_04( ):
   '''Inequality #2.'''
   r = Rational(1, 4)
   assert     r != Rational(1)
   assert     r != 1
   assert     r != 1.0
   assert not r != Rational(1, 4)
   assert not r != 0.25
   assert     r != 'foo'


def test_Rational_compare_05( ):
   '''Greater-than, #1.'''
   r = Rational(1)
   assert not r > Rational(1)
   assert not r > 1
   assert not r > 1.0
   assert     r > Rational(1, 4)
   assert     r > 0.25
   assert py.test.raises(TypeError, "r > 'foo'")


def test_Rational_compare_06( ):
   '''Greater-than, #2.'''
   r = Rational(1, 4)
   assert not r > Rational(1)
   assert not r > 1
   assert not r > 1.0
   assert not r > Rational(1, 4)
   assert not r > 0.25
   assert py.test.raises(TypeError, "r > 'foo'")


def test_Rational_compare_07( ):
   '''Greater-than-or-equal-to, #1.'''
   r = Rational(1)
   assert r >= Rational(1)
   assert r >= 1
   assert r >= 1.0
   assert r >= Rational(1, 4)
   assert r >= 0.25
   assert py.test.raises(TypeError, "r >= 'foo'")


def test_Rational_compare_08( ):
   '''Greater-than-or-equal-to, #2.'''
   r = Rational(1, 4)
   assert not r >= Rational(1)
   assert not r >= 1
   assert not r >= 1.0
   assert r >= Rational(1, 4)
   assert r >= 0.25
   assert py.test.raises(TypeError, "r >= 'foo'")


def test_Rational_compare_09( ):
   '''Less-than, #1.'''
   r = Rational(1)
   assert not r < Rational(1)
   assert not r < 1
   assert not r < 1.0
   assert not r < Rational(1, 4)
   assert not r < 0.25
   assert py.test.raises(TypeError, "r < 'foo'")


def test_Rational_compare_10( ):
   '''Less-than, #2.'''
   r = Rational(1, 4)
   assert r < Rational(1)
   assert r < 1
   assert r < 1.0
   assert not r < Rational(1, 4)
   assert not r < 0.25
   assert py.test.raises(TypeError, "r < 'foo'")


def test_Rational_compare_11( ):
   '''Less-than-or-equal-to, #1.'''
   r = Rational(1)
   assert r <= Rational(1)
   assert r <= 1
   assert r <= 1.0
   assert not r <= Rational(1, 4)
   assert not r <= 0.25
   assert py.test.raises(TypeError, "r <= 'foo'")


def test_Rational_compare_12( ):
   '''Less-than-or-equal-to, #2.'''
   r = Rational(1, 4)
   assert r <= Rational(1)
   assert r <= 1
   assert r <= 1.0
   assert r <= Rational(1, 4)
   assert r <= 0.25
   assert py.test.raises(TypeError, "r <= 'foo'")
