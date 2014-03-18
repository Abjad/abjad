# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_IOManager_view_last_log_01():
    
    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._run(pending_user_input='lvl q', is_test=True)

    assert score_manager._session.attempted_to_open_file
