from abjad import *


def test_cfgtools_get_lilypond_version_string_01( ):

   lilypond_version_string = cfgtools.get_lilypond_version_string( )
   assert isinstance(lilypond_version_string, str)
   assert lilypond_version_string.count('.') == 2
