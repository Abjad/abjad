# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_display_active_scores_01():
    
    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='q')
    string = 'Score manager - active scores'
    score_manager.session.io_transcript.last_menu_title == string
