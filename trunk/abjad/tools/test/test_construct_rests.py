from abjad import *
from abjad.tools import construct

def test_construct_rests_01( ):
   '''
   construct.rests can take a single 2-tuple as duration token.
   '''
   t = construct.rests((1,4))
   assert isinstance(t, list)
   assert len(t) == 1
   assert isinstance(t[0], Rest)
   assert t[0].duration.written == Rational(1, 4)
   assert not t[0].tie.spanned


def test_construct_rests_02( ):
   '''Tied durations result in more than one tied Rest.
   However, rests are not tied by default.'''
   t = construct.rests((5, 8))
   assert len(t) == 2
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Rest)
   assert t[0].duration.written == Rational(4, 8)
   assert t[1].duration.written == Rational(1, 8)
   assert not t[0].tie.spanned
   assert not t[1].tie.spanned


def test_construct_rests_03( ):
   '''The 'tied' keyword can be set to True to return tied Rests.  '''
   t = construct.rests((5, 8), tied=True)
   assert t[0].tie.spanner is t[1].tie.spanner


def test_construct_rests_04( ):
   '''construct.rests can take a list of duration tokens.'''
   t = construct.rests([(1, 4), Rational(1, 8)])
   assert t[0].duration.written == Rational(1, 4)
   assert t[1].duration.written == Rational(1, 8)
   assert not t[0].tie.spanned
   assert not t[1].tie.spanned
