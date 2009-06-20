from abjad import *
import py.test


def test_chord_noteheads_01( ):
   '''Returns immutable tuple of noteheads in chord.'''

   t = Chord([2, 4, 5], (1, 4))
   noteheads = t.noteheads

   assert isinstance(noteheads, tuple)
   assert len(noteheads) == 3
   assert py.test.raises(AttributeError, 'noteheads.pop( )')
   assert py.test.raises(AttributeError, 'noteheads.index(noteheads[0])')
   assert py.test.raises(AttributeError, 'noteheads.remove(noteheads[0])')


def test_chord_noteheads_02( ):
   '''Chords with equivalent pitch numbers
      *do* carry equivalent notehead instances.'''

   t1 = Chord([2, 4, 5], (1, 4))
   t2 = Chord([2, 4, 5], (1, 4))

   assert t1.numbers == t2.numbers
   assert t1.noteheads == t2.noteheads
