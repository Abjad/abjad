from abjad.chord.chord import Chord
from abjad.note.note import Note
from abjad.rest.rest import Rest


def chord_cast_defective(chord):
   assert isinstance(chord, Chord)
   if len(chord) == 0:
      return Rest(chord)
   elif len(chord) == 1:
      return Note(chord)
   else:
      return chord
