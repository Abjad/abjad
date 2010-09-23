from abjad.cfg.cfg import ABJADVERSIONFILE


def get_abjad_version_string( ):
   '''Get Abjad vesion string:

   ::

      abjad> iotools.get_abjad_version_string( )
      '3702'
   '''

   return file(ABJADVERSIONFILE, 'r').read( ).strip( )
