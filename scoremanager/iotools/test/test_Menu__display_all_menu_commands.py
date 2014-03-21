# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu__display_all_menu_commands_01():
    
    score_manager = scoremanager.core.ScoreManager()
    input_ = '? q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.last_menu_lines[-2] != ''
    assert score_manager._transcript.last_menu_lines[-1] == ''