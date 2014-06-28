# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageWrangler__make_main_menu_01():

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._is_test = True
    statement = 'ide._score_package_wrangler._make_main_menu()'
    count = ide._session.io_manager.count_function_calls(
        statement,
        global_context=globals(),
        local_context=locals(),
        )

    assert count < 4600