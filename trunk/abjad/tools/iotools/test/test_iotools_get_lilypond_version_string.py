from abjad import *


def test_iotools_get_lilypond_version_string_01( ):

   lilypond_version_string = iotools.get_lilypond_version_string( )
   assert isinstance(lilypond_version_string, str)
   assert lilypond_version_string.count('.') == 2
