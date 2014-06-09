# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_StylesheetWrangler_display_session_variables_01():
    
    input_ = 'red~example~score y sv q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'command_history' in contents
    assert 'controller_stack' in contents


def test_StylesheetWrangler_display_session_variables_02():
    
    input_ = 'y sv q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'command_history' in contents
    assert 'controller_stack' in contents