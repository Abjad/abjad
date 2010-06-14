from abjad import *


def test_leaftools_make_rests_01( ):
   '''
   leaftools.make_rests can take a single 2-tuple as duration token.
   '''
   t = leaftools.make_rests((1,4))
   assert isinstance(t, list)
   assert len(t) == 1
   assert isinstance(t[0], Rest)
   assert t[0].duration.written == Rational(1, 4)
   assert not t[0].tie.spanned


def test_leaftools_make_rests_02( ):
   '''Tied durations result in more than one tied Rest.
   However, rests are not tied by default.'''
   t = leaftools.make_rests((5, 8))
   assert len(t) == 2
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Rest)
   assert t[0].duration.written == Rational(4, 8)
   assert t[1].duration.written == Rational(1, 8)
   assert not t[0].tie.spanned
   assert not t[1].tie.spanned


def test_leaftools_make_rests_03( ):
   '''The 'tied' keyword can be set to True to return tied Rests.  '''
   t = leaftools.make_rests((5, 8), tied=True)
   assert t[0].tie.spanner is t[1].tie.spanner


def test_leaftools_make_rests_04( ):
   '''leaftools.make_rests can take a list of duration tokens.'''
   t = leaftools.make_rests([(1, 4), Rational(1, 8)])
   assert t[0].duration.written == Rational(1, 4)
   assert t[1].duration.written == Rational(1, 8)
   assert not t[0].tie.spanned
   assert not t[1].tie.spanned
