# -*- encoding: utf-8 -*-
import pytest
pytest.skip('unskip after returning summary menu to tempo editing screen.')
from abjad import *
import scoremanager


def test_MenuSection__make_menu_lines_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=input_)

    string = '  * 8=72'
    assert score_manager._transcript.last_menu_lines[2] == string