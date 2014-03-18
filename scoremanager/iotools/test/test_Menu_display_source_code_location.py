# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu_display_source_code_location_01():
    r'''Sets is_test=False to run with source code tracking turned on.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run('scl q', is_test=False)

    menu_lines = score_manager._transcript.last_menu_lines
    assert 'file' in menu_lines[0]
    assert 'method' in menu_lines[1]
    assert 'line' in menu_lines[2]
