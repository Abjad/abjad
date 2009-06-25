from abjad.pitch.pitch import Pitch


def change_default_accidental_spelling(spelling = 'mixed'):
   '''.. versionadded:: 1.1.2

   Change default accidental spelling. ::

      abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
      [Note(cs'', 5), Note(ef'', 5)]

   ::

      abjad> pitchtools.change_default_accidental_spelling('sharps')
      abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
      [Note(cs'', 5), Note(ds'', 5)]

   ::

      abjad> pitchtools.change_default_accidental_spelling('flats')
      abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
      [Note(df'', 5), Note(ef'', 5)]

   Call with ``spelling = 'mixed'`` or with empty argument list
   to revert back to default mixed spelling. ::

      abjad> pitchtools.change_default_accidental_spelling('mixed')
      abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
      [Note(cs'', 5), Note(ef'', 5)]
   '''
   
   if spelling not in ('mixed', 'sharps', 'flats'):
      raise ValueError

   Pitch.accidental_spelling = spelling
