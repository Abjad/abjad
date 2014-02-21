# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_view_cache_01():
    
    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='cv q', is_test=True)

    assert score_manager._session.attempted_to_open_file
