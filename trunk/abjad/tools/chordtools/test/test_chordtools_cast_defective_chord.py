from abjad import *


def test_chordtools_cast_defective_chord_01( ):
   '''Cast zero-length chord as rest.'''

   t = Chord([ ], (1, 8))
   rest = chordtools.cast_defective_chord(t)

   assert isinstance(t, Chord)
   assert isinstance(rest, Rest)


def test_chordtools_cast_defective_chord_02( ):
   '''Cast length-one chord as note.'''

   t = Chord([0], (1, 8))
   note = chordtools.cast_defective_chord(t)

   assert isinstance(t, Chord)
   assert isinstance(note, Note)


def test_chordtools_cast_defective_chord_03( ):
   '''Return notes and rests unchanged.'''

   note = Note(0, (1, 4))
   assert chordtools.cast_defective_chord(note) is note

   rest = Rest((1, 4))
   assert chordtools.cast_defective_chord(rest) is rest
