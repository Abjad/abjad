from abjad.tools.chordtools.Chord import Chord


def change_defective_chord_to_note_or_rest(chord):
   '''.. versionadded:: 1.1.1

   Change zero-length `chord` to rest::

      abjad> chord = Chord([ ], (3, 16))

   ::

      abjad> chord
      Chord('<>8.')

   ::

      abjad> chordtools.change_defective_chord_to_note_or_rest(chord)
      Rest('r8.')

   Change length-one chord to note::

      abjad> chord = Chord("<cs''>8.")

   ::

      abjad> chord
      Chord("<cs''>8.")

   ::

      abjad> chordtools.change_defective_chord_to_note_or_rest(chord)
      Note("cs''8.")

   Return chords with length greater than one unchanged::

      abjad> chord = Chord("<c' c'' cs''>8.")

   ::

      abjad> chord
      Chord("<c' c'' cs''>8.")

   ::

      abjad> chordtools.change_defective_chord_to_note_or_rest(chord)
      Chord("<c' c'' cs''>8.")

   Return notes unchanged::

      abjad> note = Note("c'4")

   ::

      abjad> note
      Note("c'4")

   ::

      abjad> chordtools.change_defective_chord_to_note_or_rest(note)
      Note("c'4")

   Return rests unchanged::

      abjad> rest = Rest('r4')

   ::

      abjad> rest
      Rest('r4')

   ::

      abjad> chordtools.change_defective_chord_to_note_or_rest(rest)
      Rest('r4')

   Return note, rest, chord or none.

   .. versionchanged:: 1.1.2
      renamed ``chordtools.cast_defective( )`` to
      ``chordtools.change_defective_chord_to_note_or_rest( )``.
   '''
   from abjad.tools import resttools
   from abjad.tools import notetools

   if isinstance(chord, Chord):
      if len(chord) == 0:
         return resttools.Rest(chord)
      elif len(chord) == 1:
         return notetools.Note(chord)

   return chord
