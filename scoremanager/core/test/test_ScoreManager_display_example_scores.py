# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_display_example_scores_01():
    
    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'ssx q'
    score_manager._run(pending_user_input=input_)

    string = 'Score manager - example scores'
    assert score_manager._transcript.last_title == string
