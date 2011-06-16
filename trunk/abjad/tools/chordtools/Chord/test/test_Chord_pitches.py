from abjad import *
import py.test


def test_Chord_pitches_01( ):
   '''Returns immutable tuple of pitches in chord.
   '''

   t = Chord([2, 4, 5], (1, 4))
   pitches = t.pitches

   assert isinstance(pitches, tuple)
   assert len(pitches) == 3
   assert py.test.raises(AttributeError, 'pitches.pop( )')
   assert py.test.raises(AttributeError, 'pitches.remove(pitches[0])')


def test_Chord_pitches_02( ):
   '''Chords with equivalent numbers carry equivalent pitches.
   '''

   t1 = Chord([2, 4, 5], (1, 4))
   t2 = Chord([2, 4, 5], (1, 4))

   assert t1.pitches == t2.pitches
