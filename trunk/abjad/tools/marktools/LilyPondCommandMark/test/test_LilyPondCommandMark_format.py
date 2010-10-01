from abjad import *


def test_LilyPondCommandMark_format_01( ):

   command_mark = marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")
   
   assert command_mark.format == "#(set-accidental-style 'forget)"
