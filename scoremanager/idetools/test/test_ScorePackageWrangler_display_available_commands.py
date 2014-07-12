# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_display_available_commands_01():
    r'''Displays correct title.
    '''
    
    input_ = '?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Abjad IDE - scores - available commands' in contents


def test_ScorePackageWrangler_display_available_commands_02():
    r'''Displays only one blank line after title.
    '''
    
    input_ = '?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    title = 'Abjad IDE - scores - available commands'
    first_blank_line = ''
    first_real_line = '    all packages -'
    string = '\n'.join([title, first_blank_line, first_real_line])
    assert string in contents