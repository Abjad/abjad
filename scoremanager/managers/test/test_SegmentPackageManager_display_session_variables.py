# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_display_session_variables_01():
    
    input_ = 'red~example~score g A sv q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'command_history' in contents
    assert 'controller_stack' in contents