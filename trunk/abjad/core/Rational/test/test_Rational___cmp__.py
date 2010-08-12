from abjad import *
import py.test


def test_Rational___cmp___01( ):
   '''Equality #1.'''
   r = Rational(1)
   assert     r == Rational(1)
   assert     r == 1
   assert     r == 1.0
   assert not r == Rational(1, 4)
   assert not r == 0.25
   assert not r == 'foo'


def test_Rational___cmp___02( ):
   '''Equality #2.'''
   r = Rational(1, 4)
   assert not r == Rational(1)
   assert not r == 1
   assert not r == 1.0
   assert     r == Rational(1, 4)
   assert     r == 0.25
   assert not r == 'foo'


def test_Rational___cmp___03( ):
   '''Inequality #1.'''
   r = Rational(1)
   assert not r != Rational(1)
   assert not r != 1
   assert not r != 1.0
   assert     r != Rational(1, 4)
   assert     r != 0.25
   assert     r != 'foo'


def test_Rational___cmp___04( ):
   '''Inequality #2.'''
   r = Rational(1, 4)
   assert     r != Rational(1)
   assert     r != 1
   assert     r != 1.0
   assert not r != Rational(1, 4)
   assert not r != 0.25
   assert     r != 'foo'


def test_Rational___cmp___05( ):
   '''Greater-than, #1.'''
   r = Rational(1)
   assert not r > Rational(1)
   assert not r > 1
   assert not r > 1.0
   assert     r > Rational(1, 4)
   assert     r > 0.25
   assert py.test.raises(TypeError, "r > 'foo'")


def test_Rational___cmp___06( ):
   '''Greater-than, #2.'''
   r = Rational(1, 4)
   assert not r > Rational(1)
   assert not r > 1
   assert not r > 1.0
   assert not r > Rational(1, 4)
   assert not r > 0.25
   assert py.test.raises(TypeError, "r > 'foo'")


def test_Rational___cmp___07( ):
   '''Greater-than-or-equal-to, #1.'''
   r = Rational(1)
   assert r >= Rational(1)
   assert r >= 1
   assert r >= 1.0
   assert r >= Rational(1, 4)
   assert r >= 0.25
   assert py.test.raises(TypeError, "r >= 'foo'")


def test_Rational___cmp___08( ):
   '''Greater-than-or-equal-to, #2.'''
   r = Rational(1, 4)
   assert not r >= Rational(1)
   assert not r >= 1
   assert not r >= 1.0
   assert r >= Rational(1, 4)
   assert r >= 0.25
   assert py.test.raises(TypeError, "r >= 'foo'")


def test_Rational___cmp___09( ):
   '''Less-than, #1.'''
   r = Rational(1)
   assert not r < Rational(1)
   assert not r < 1
   assert not r < 1.0
   assert not r < Rational(1, 4)
   assert not r < 0.25
   assert py.test.raises(TypeError, "r < 'foo'")


def test_Rational___cmp___10( ):
   '''Less-than, #2.'''
   r = Rational(1, 4)
   assert r < Rational(1)
   assert r < 1
   assert r < 1.0
   assert not r < Rational(1, 4)
   assert not r < 0.25
   assert py.test.raises(TypeError, "r < 'foo'")


def test_Rational___cmp___11( ):
   '''Less-than-or-equal-to, #1.'''
   r = Rational(1)
   assert r <= Rational(1)
   assert r <= 1
   assert r <= 1.0
   assert not r <= Rational(1, 4)
   assert not r <= 0.25
   assert py.test.raises(TypeError, "r <= 'foo'")


def test_Rational___cmp___12( ):
   '''Less-than-or-equal-to, #2.'''
   r = Rational(1, 4)
   assert r <= Rational(1)
   assert r <= 1
   assert r <= 1.0
   assert r <= Rational(1, 4)
   assert r <= 0.25
   assert py.test.raises(TypeError, "r <= 'foo'")
