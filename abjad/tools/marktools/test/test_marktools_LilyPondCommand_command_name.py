# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_LilyPondCommand_command_name_01():
    r'''LilyPondCommand command name is read / write.
    '''

    lilypond_command = marktools.LilyPondCommand('slurDotted')
    assert lilypond_command.name == 'slurDotted'

    lilypond_command.name = 'slurDashed'
    assert lilypond_command.name == 'slurDashed'
