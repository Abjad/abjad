# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_view_cache_01():
    
    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'cv q'
    score_manager._run(pending_user_input=input_)

    assert score_manager._session.attempted_to_open_file
