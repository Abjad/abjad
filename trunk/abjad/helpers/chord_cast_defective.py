from abjad.chord.chord import Chord
from abjad.note.note import Note
from abjad.rest.rest import Rest


def chord_cast_defective(chord):
   '''Cast zero-length chord to rest.
      Cast length-one chord to note.
      Return chords with length greater than one unchanged.'''

   assert isinstance(chord, Chord)

   if len(chord) == 0:
      return Rest(chord)
   elif len(chord) == 1:
      return Note(chord)
   else:
      return chord
