from abjad.components.Chord import Chord
from abjad.components.Note import Note
from abjad.components.Rest import Rest


def cast_defective_chord(chord):
   '''Cast zero-length `chord` to rest. ::

      abjad> chord = Chord([ ], (3, 16))
      abjad> chord
      Chord(, 8.)
      abjad> chordtools.cast_defective_chord(chord)
      Rest(8.)

   Cast length-one chord to note. ::

      abjad> chord = Chord([13], (3, 16))
      abjad> chord
      Chord(cs'', 8.)
      abjad> chordtools.cast_defective_chord(chord)
      Note(cs'', 8.)

   Return chords with length greater than one unchanged. ::

      abjad> chord = Chord([0, 12, 13], (3, 16))
      abjad> chord
      Chord(c' c'' cs'', 8.)
      abjad> chordtools.cast_defective_chord(chord)
      Chord(c' c'' cs'', 8.)

   Return notes and rests unchanged. ::

      abjad> note = Note(0, (1, 4))
      abjad> chordtools.cast_defective_chord(note)
      Note(c', 4)

   ::

      abjad> rest = Rest((1, 4))
      abjad> chordtools.cast_defective_chord(rest)
      Rest((1, 4))

   .. versionchanged:: 1.1.2
      renamed ``chordtools.cast_defective( )`` to
      ``chordtools.cast_defective_chord( )``.
   '''

   if isinstance(chord, Chord):
      if len(chord) == 0:
         return Rest(chord)
      elif len(chord) == 1:
         return Note(chord)

   return chord
