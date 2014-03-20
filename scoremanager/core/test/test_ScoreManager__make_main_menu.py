# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager__make_main_menu_01():
    r'''Performance. Sets is_test=True to run with source code tracking
    turned off.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_test = True
    statement = 'score_manager._make_main_menu()'
    count = score_manager._session.io_manager.count_function_calls(
        statement,
        global_context=globals(),
        local_context=locals(),
        )

    assert count < 3200