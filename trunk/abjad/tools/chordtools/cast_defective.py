from abjad.chord import Chord
from abjad.note import Note
from abjad.rest import Rest


def cast_defective(chord):
   '''Cast zero-length `chord` to rest. ::

      abjad> chord = Chord([ ], (3, 16))
      abjad> chord
      Chord(, 8.)
      abjad> chordtools.cast_defective(chord)
      Rest(8.)

   Cast length-one chord to note. ::

      abjad> chord = Chord([13], (3, 16))
      abjad> chord
      Chord(cs'', 8.)
      abjad> chordtools.cast_defective(chord)
      Note(cs'', 8.)

   Return chords with length greater than one unchanged. ::

      abjad> chord = Chord([0, 12, 13], (3, 16))
      abjad> chord
      Chord(c' c'' cs'', 8.)
      abjad> chordtools.cast_defective(chord)
      Chord(c' c'' cs'', 8.)
   '''

   assert isinstance(chord, Chord)

   if len(chord) == 0:
      return Rest(chord)
   elif len(chord) == 1:
      return Note(chord)
   else:
      return chord
