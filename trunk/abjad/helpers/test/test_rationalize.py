from abjad import *
from py.test import raises

def test_rationalize_01( ):
   '''Rationalize can take a list of duples.'''
   l = [(i, 16) for i in range(1, 9)]
   t = rationalize(l)
   for i, e in enumerate(t):
      assert isinstance(e, Rational)
      assert e == Rational(i+1, 16)


def test_rationalize_02( ):
   '''Rationalize can take a list of duples and Rationals.'''
   l = [(i, 16) for i in range(1, 5)]
   l.extend([Rational(i, 16) for i in range(5, 9)])
   t = rationalize(l)
   for i, e in enumerate(t):
      assert isinstance(e, Rational)
      assert e == Rational(i+1, 16)


def test_rationalize_03( ):
   '''Rationalize can take nested lists.'''
   l = [(i, 16) for i in range(1, 9)]
   l.insert(4, [(i, 16) for i in range(1, 9)])
   t = rationalize(l)
   for i, e in enumerate(t[0:4]):
      assert isinstance(e, Rational)
      assert e == Rational(i+1, 16)
   for i, e in enumerate(t[5:]):
      assert isinstance(e, Rational)
      assert e == Rational(i+1+4, 16)
   for i, e in enumerate(t[4]):
      assert isinstance(e, Rational)
      assert e == Rational(i+1, 16)


def test_rationalize_04( ):
   '''Elements in list must be duration tokens, so (0, n) is invalid.'''
   assert raises(AssertionError, 'rationalize([ (0, 4) ])')
