# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_edit_views_py_01():

    input_ = 'yy we q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file