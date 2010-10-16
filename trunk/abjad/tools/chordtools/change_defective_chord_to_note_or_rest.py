from abjad.components.Chord import Chord
from abjad.components.Note import Note
from abjad.components.Rest import Rest


def change_defective_chord_to_note_or_rest(chord):
   '''Change zero-length `chord` to rest. ::

      abjad> chord = Chord([ ], (3, 16))
      abjad> chord
      Chord(, 8.)
      abjad> chordtools.change_defective_chord_to_note_or_rest(chord)
      Rest(8.)

   Change length-one chord to note. ::

      abjad> chord = Chord([13], (3, 16))
      abjad> chord
      Chord(cs'', 8.)
      abjad> chordtools.change_defective_chord_to_note_or_rest(chord)
      Note(cs'', 8.)

   Return chords with length greater than one unchanged. ::

      abjad> chord = Chord([0, 12, 13], (3, 16))
      abjad> chord
      Chord(c' c'' cs'', 8.)
      abjad> chordtools.change_defective_chord_to_note_or_rest(chord)
      Chord(c' c'' cs'', 8.)

   Return notes and rests unchanged. ::

      abjad> note = Note(0, (1, 4))
      abjad> chordtools.change_defective_chord_to_note_or_rest(note)
      Note(c', 4)

   ::

      abjad> rest = Rest((1, 4))
      abjad> chordtools.change_defective_chord_to_note_or_rest(rest)
      Rest((1, 4))

   .. versionchanged:: 1.1.2
      renamed ``chordtools.cast_defective( )`` to
      ``chordtools.change_defective_chord_to_note_or_rest( )``.
   '''

   if isinstance(chord, Chord):
      if len(chord) == 0:
         return Rest(chord)
      elif len(chord) == 1:
         return Note(chord)

   return chord
