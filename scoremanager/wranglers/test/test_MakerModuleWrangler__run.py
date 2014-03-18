# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MakerModuleWrangler__run_01():
    
    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score k q'
    score_manager._run(pending_user_input=input_, is_test=True)
    line = '     1: RedExampleScoreTemplate.py'
    assert line in score_manager._transcript.last_menu_lines
