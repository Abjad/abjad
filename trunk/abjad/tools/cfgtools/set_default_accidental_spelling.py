from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


def set_default_accidental_spelling(spelling = 'mixed'):
   '''.. versionadded:: 1.1.1

   Set default accidental spelling to mixed::

      abjad> cfgtools.set_default_accidental_spelling( )

   ::

      abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
      [Note(cs'', 5), Note(ef'', 5)]

   Set default accidental spelling to sharps::

      abjad> cfgtools.set_default_accidental_spelling('sharps')

   ::

      abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
      [Note(cs'', 5), Note(ds'', 5)]

   Set default accidental spelling to flats::

      abjad> cfgtools.set_default_accidental_spelling('flats')

   ::

      abjad> [Note(13, (1, 4)), Note(15, (1, 4))]
      [Note(df'', 5), Note(ef'', 5)]

   Return none.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.change_default_accidental_spelling( )`` to
      ``cfgtools.set_default_accidental_spelling( )``.
   '''
   
   if spelling not in ('mixed', 'sharps', 'flats'):
      raise ValueError

   NamedChromaticPitch.accidental_spelling = spelling
