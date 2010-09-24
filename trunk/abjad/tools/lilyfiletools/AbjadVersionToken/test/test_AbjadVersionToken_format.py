from abjad import *


def test_AbjadVersionToken_format_01( ):

   abjad_version_token = lilyfiletools.AbjadVersionToken( )
   assert isinstance(abjad_version_token.format, str)
