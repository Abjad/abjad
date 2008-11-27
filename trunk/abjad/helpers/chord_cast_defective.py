from abjad.chord.chord import Chord
from abjad.note.note import Note
from abjad.skip.skip import Skip


def chord_cast_defective(chord):
   assert isinstance(chord, Chord)
   if len(chord) == 0:
      return Skip(chord)
   elif len(chord) == 1:
      return Note(chord)
   else:
      return chord
