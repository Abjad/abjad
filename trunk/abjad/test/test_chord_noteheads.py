from abjad import *
from py.test import raises


def test_chord_noteheads_01( ):
   '''Returns immutable tuple of noteheads in chord.'''
   t = Chord([2, 4, 5], (1, 4))
   noteheads = t.noteheads
   assert isinstance(noteheads, tuple)
   assert len(noteheads) == 3
   assert raises(AttributeError, 'noteheads.pop( )')
   assert raises(AttributeError, 'noteheads.index(noteheads[0])')
   assert raises(AttributeError, 'noteheads.remove(noteheads[0])')


def test_chord_noteheads_02( ):
   '''Chords with equivalent pitch numbers
      do not carry equivalent notehead instances.'''
   t1 = Chord([2, 4, 5], (1, 4))
   t2 = Chord([2, 4, 5], (1, 4))
   assert t1.numbers == t2.numbers
   assert not t1.noteheads == t2.noteheads
