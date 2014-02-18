# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu_display_source_code_location_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run('ltt scl q')

    menu_lines = score_manager.session.io_transcript[-2][1]
    assert 'file' in menu_lines[0]
    assert 'method' in menu_lines[1]
    assert 'line' in menu_lines[2]
