from abjad import *
import py.test


def test_chord_note_heads_01( ):
   '''Returns immutable tuple of note_heads in chord.'''

   t = Chord([2, 4, 5], (1, 4))
   note_heads = t.note_heads

   assert isinstance(note_heads, tuple)
   assert len(note_heads) == 3
   assert py.test.raises(AttributeError, 'note_heads.pop( )')
   ## Python 2.6 implements tuple.index( )
   #assert py.test.raises(AttributeError, 'note_heads.index(note_heads[0])')
   assert py.test.raises(AttributeError, 'note_heads.remove(note_heads[0])')


def test_chord_note_heads_02( ):
   '''Chords with equivalent pitch numbers
   *do* carry equivalent note_head instances.'''

   t1 = Chord([2, 4, 5], (1, 4))
   t2 = Chord([2, 4, 5], (1, 4))

   assert t1.numbers == t2.numbers
   assert t1.note_heads == t2.note_heads


def test_chord_note_heads_03( ):
   '''Note head can be assigned with a LilyPond-style
   note name string.'''

   t = Chord([0], (1, 4))
   t.note_heads = "c' d' e'"

   assert t.format == "<c' d' e'>4"
