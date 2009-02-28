from abjad import *

def test_rationalize_01( ):
   '''Rationalize can take a list of duples.'''
   l = [(i, 16) for i in range(8)]
   t = rationalize(l)
   for i, e in enumerate(t):
      assert isinstance(e, Rational)
      assert e == Rational(i, 16)


def test_rationalize_02( ):
   '''Rationalize can take a list of duples and Rationals.'''
   l = [(i, 16) for i in range(4)]
   l.extend([Rational(i, 16) for i in range(4, 8)])
   t = rationalize(l)
   for i, e in enumerate(t):
      assert isinstance(e, Rational)
      assert e == Rational(i, 16)


def test_rationalize_03( ):
   '''Rationalize can take nested lists.'''
   l = [(i, 16) for i in range(8)]
   l.insert(4, [(i, 16) for i in range(8)])
   t = rationalize(l)
   for i, e in enumerate(t[0:4]):
      assert isinstance(e, Rational)
      assert e == Rational(i, 16)
   for i, e in enumerate(t[5:]):
      assert isinstance(e, Rational)
      assert e == Rational(i+4, 16)
   for i, e in enumerate(t[4]):
      assert isinstance(e, Rational)
      assert e == Rational(i, 16)


