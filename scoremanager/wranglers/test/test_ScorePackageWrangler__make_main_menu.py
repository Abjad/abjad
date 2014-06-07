# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageWrangler__make_main_menu_01():

    score_manager = scoremanager.core.AbjadIDE(is_test=True)
    score_manager._session._is_test = True
    statement = 'score_manager._score_package_wrangler._make_main_menu()'
    count = score_manager._session.io_manager.count_function_calls(
        statement,
        global_context=globals(),
        local_context=locals(),
        )

    assert count < 4200