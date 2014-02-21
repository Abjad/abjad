# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu_display_hidden_menu_commands_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='n q')

    string = 'Score manager - example scores - hidden commands'
    assert score_manager._session.transcript.last_menu_title == string


def test_Menu_display_hidden_menu_commands_02():
    r'''Hidden menu persists after junk.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='n asdf q')

    string = 'Score manager - example scores - hidden commands'
    transcript = score_manager._session.transcript

    assert transcript.system_display_entries[-1].title == string
    assert transcript.system_display_entries[-2].title == string


def test_Menu_display_hidden_menu_commands_03():
    r'''Hidden menu persists after 'LilyPond log view.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='n lvl q')

    string = 'Score manager - example scores - hidden commands'
    transcript = score_manager._session.transcript

    assert transcript.system_display_entries[-1].title == string
    assert transcript.system_display_entries[-2].title == string
