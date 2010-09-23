from abjad import *


def test_iotools_get_abjad_version_string_01( ):

   assert isinstance(iotools.get_abjad_version_string( ), str)
