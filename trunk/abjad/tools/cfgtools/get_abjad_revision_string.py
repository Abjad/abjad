from abjad.cfg.cfg import ABJADVERSIONFILE


def get_abjad_revision_string( ):
   '''.. versionadded:: 1.1.2

   Get Abjad revision string::

      abjad> cfgtools.get_abjad_revision_string( ) # doctest: +SKIP
      '4392'

   Return string.
   '''

   return file(ABJADVERSIONFILE, 'r').read( ).strip( )
