from abjad import *
from py.test import raises


def test_chord_pitches_01( ):
   '''Returns immutable tuple of pitches in chord.'''
   t = Chord([2, 4, 5], (1, 4))
   pitches = t.pitches
   assert isinstance(pitches, tuple)
   assert len(pitches) == 3
   assert raises(AttributeError, 'pitches.pop( )')
   assert raises(AttributeError, 'pitches.index(pitches[0])')
   assert raises(AttributeError, 'pitches.remove(pitches[0])')


def test_chord_pitches_02( ):
   '''Chords with equivalent numbers 
      do not carry equivalent pitch instances.'''
   t1 = Chord([2, 4, 5], (1, 4))
   t2 = Chord([2, 4, 5], (1, 4))
   assert t1.numbers == t2.numbers
   assert not t1.pitches == t2.pitches
