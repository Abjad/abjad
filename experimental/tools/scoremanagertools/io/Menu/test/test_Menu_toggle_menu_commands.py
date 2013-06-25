from experimental import *


def test_Menu_toggle_menu_commands_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='tmc q')

    starting_menu_lines = score_manager.session.transcript[0][1]
    modified_menu_lines = score_manager.session.transcript[2][1]

    new_score_menu_line = '     new score (new)'
    assert new_score_menu_line in starting_menu_lines
    assert not new_score_menu_line in modified_menu_lines
