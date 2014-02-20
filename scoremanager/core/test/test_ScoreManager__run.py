# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager__run_01():
    r'''Start-up performance.
    '''

    score_manager = scoremanager.core.ScoreManager()
    statement = "score_manager._run(pending_user_input='q')"
    count = score_manager.session.io_manager.count_function_calls(
        statement,
        global_context=globals(),
        local_context=locals(),
        )

    assert count < 15000
