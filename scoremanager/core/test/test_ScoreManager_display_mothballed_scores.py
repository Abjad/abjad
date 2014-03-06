# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_display_mothballed_scores_01():
    
    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='ssmb q', is_test=True)

    string = 'Score manager - mothballed scores'
    assert score_manager._transcript.last_title == string
