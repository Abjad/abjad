from abjad import *


def test_iotools_get_lilypond_version_01( ):

   lilypond_version = iotools.get_lilypond_version( )
   assert isinstance(lilypond_version, str)
   assert lilypond_version.count('.') == 2
