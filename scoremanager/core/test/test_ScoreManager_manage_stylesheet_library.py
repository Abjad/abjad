# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_manage_stylesheet_library_01():
    
    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'lmy q'
    score_manager._run(pending_user_input=input_)

    string = 'Score manager - stylesheet library'
    assert score_manager._transcript.last_title == string
