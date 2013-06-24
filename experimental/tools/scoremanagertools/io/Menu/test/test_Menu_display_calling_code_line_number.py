from experimental import *


def test_Menu_display_calling_code_line_number_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run('twt where q')

    menu_lines = score_manager._session.transcript[-2][1]
    assert 'file' in menu_lines[0]
    assert 'method' in menu_lines[1]
    assert 'line' in menu_lines[2]
