# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MenuSection__make_menu_lines_01():

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=input_)

    string = '  * Tempo(Duration(1, 8), 72)'
    assert score_manager._transcript.last_menu_lines[2] == string