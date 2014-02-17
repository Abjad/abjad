# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu_display_calling_code_line_number_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run('wtt where q')

    menu_lines = score_manager.session.io_transcript[-2][1]
    assert 'file' in menu_lines[0]
    assert 'method' in menu_lines[1]
    assert 'line' in menu_lines[2]
