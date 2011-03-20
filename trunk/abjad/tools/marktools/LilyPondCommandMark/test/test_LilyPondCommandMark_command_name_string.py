from abjad import *


def test_LilyPondCommandMark_command_name_string_01( ):
   '''LilyPondCommandMark command name string is read / write.
   '''

   lilypond_command = marktools.LilyPondCommandMark('slurDotted')
   assert lilypond_command.command_name_string == 'slurDotted'

   lilypond_command.command_name_string = 'slurDashed'
   assert lilypond_command.command_name_string == 'slurDashed'
