# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu_display_source_code_location_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run('sct default scl q')

    menu_lines = score_manager._session.io_transcript.last_menu_lines
    assert 'file' in menu_lines[0]
    assert 'method' in menu_lines[1]
    assert 'line' in menu_lines[2]
