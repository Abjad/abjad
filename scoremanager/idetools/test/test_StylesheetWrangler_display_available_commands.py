# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_display_available_commands_01():
    
    input_ = 'red~example~score y ?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'stylesheets directory - available commands' in contents


def test_StylesheetWrangler_display_available_commands_02():
    
    input_ = 'yy ?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Abjad IDE - stylesheets depot - available commands' in contents