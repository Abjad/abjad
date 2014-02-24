# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_display_example_scores_01():
    
    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='ssx q')

    string = 'Score manager - example scores'
    assert score_manager._transcript.last_menu_title == string
