# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_display_avialable_commands_01():
    
    input_ = 'red~example~score k ?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'maker files - available commands' in contents


def test_MakerFileWrangler_display_avialable_commands_02():
    
    input_ = 'K ?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Abjad IDE - maker files - available commands' in contents