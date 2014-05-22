# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_display_available_commands_01():
    
    input_ = 'red~example~score u ? q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'build files - available commands' in contents


def test_BuildFileWrangler_display_available_commands_02():
    
    input_ = 'u ? q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'Score Manager - build files - available commands' in contents