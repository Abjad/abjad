# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu_toggle_menu_commands_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='mct default q')

    starting_menu_lines = score_manager.session.io_transcript[0][1]
    modified_menu_lines = score_manager.session.io_transcript[2][1]

    new_score_menu_line = '     new score (new)'
    assert new_score_menu_line in starting_menu_lines
    assert not new_score_menu_line in modified_menu_lines
