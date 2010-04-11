from abjad import *
from py.test import raises


def test_chord_pairs_01( ):
   '''Returns sorted immutable tuple of pitch pairs in chord.'''
   t = Chord([2, 4, 5], (1, 4))
   pairs = t.pairs
   assert pairs == (('d', 4), ('e', 4), ('f', 4))
   assert raises(AttributeError, 'pairs.pop( )')
   ## Python 2.6 implements tuple.index( )
   #assert raises(AttributeError, 'pairs.index(pairs[0])')
   assert raises(AttributeError, 'pairs.remove(pairs[0])')


def test_chord_pairs_02( ):
   '''Chords with equivalent pairs do carry equivalent pitch pair tuples.'''
   t1 = Chord([2, 4, 5], (1, 4))
   t2 = Chord([2, 4, 5], (1, 4))
   assert t1.pairs == t2.pairs
