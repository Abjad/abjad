from abjad.cfg.cfg import ABJADVERSIONFILE


def _get_abjad_version( ):
   return file(ABJADVERSIONFILE, 'r').read( ).strip( )
