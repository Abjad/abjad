# -*- encoding: utf-8 -*-
import sys
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

    if sys.version_info[0] == 2:
        assert count < 9000
    else:
        assert count < 10000