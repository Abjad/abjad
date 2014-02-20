# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager__make_main_menu_01():
    r'''Performance.
    '''

    score_manager = scoremanager.core.ScoreManager()
    statement = 'score_manager._make_main_menu()'
    count = score_manager.session.io_manager.count_function_calls(
        statement,
        global_context=globals(),
        local_context=locals(),
        )

    assert count < 2000
