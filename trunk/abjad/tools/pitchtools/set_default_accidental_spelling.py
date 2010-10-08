from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


def set_default_accidental_spelling(spelling = 'mixed'):
   '''.. versionadded:: 1.1.1

   Change default accidental spelling. ::

      abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
      [Note(cs'', 5), Note(ef'', 5)]

   ::

      abjad> pitchtools.set_default_accidental_spelling('sharps')
      abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
      [Note(cs'', 5), Note(ds'', 5)]

   ::

      abjad> pitchtools.set_default_accidental_spelling('flats')
      abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
      [Note(df'', 5), Note(ef'', 5)]

   Call with ``spelling = 'mixed'`` or with empty argument list
   to revert back to default mixed spelling. ::

      abjad> pitchtools.set_default_accidental_spelling('mixed')
      abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
      [Note(cs'', 5), Note(ef'', 5)]

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.change_default_accidental_spelling( )`` to
      ``pitchtools.set_default_accidental_spelling( )``.
   '''
   
   if spelling not in ('mixed', 'sharps', 'flats'):
      raise ValueError

   NamedChromaticPitch.accidental_spelling = spelling
