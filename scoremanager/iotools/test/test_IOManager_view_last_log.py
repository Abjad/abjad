# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_IOManager_view_last_log_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'll q'
    score_manager._run(pending_user_input=input_)

    assert score_manager._session._attempted_to_open_file