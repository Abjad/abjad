# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler__handle_numeric_user_input_01():

    input_ = 'red~example~score u 1 q'
    score_manager._run(pending_input=input_)

    assert score_manager._session._attempted_to_open_file