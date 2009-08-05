from abjad import *


def test_chordtools_cast_defective_01( ):
   '''Cast zero-length chord as rest.'''

   t = Chord([ ], (1, 8))
   rest = chordtools.cast_defective(t)

   assert isinstance(t, Chord)
   assert isinstance(rest, Rest)


def test_chordtools_cast_defective_02( ):
   '''Cast length-one chord as note.'''

   t = Chord([0], (1, 8))
   note = chordtools.cast_defective(t)

   assert isinstance(t, Chord)
   assert isinstance(note, Note)
