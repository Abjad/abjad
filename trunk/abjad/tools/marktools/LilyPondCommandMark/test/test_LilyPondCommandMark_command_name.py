# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondCommandMark_command_name_01():
    r'''LilyPondCommandMark command name is read / write.
    '''

    lilypond_command = marktools.LilyPondCommandMark('slurDotted')
    assert lilypond_command.command_name == 'slurDotted'

    lilypond_command.command_name = 'slurDashed'
    assert lilypond_command.command_name == 'slurDashed'
