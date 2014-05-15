# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu__display_all_menu_commands_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = '? q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'system - commands' in contents
    assert 'scores - new' in contents


def test_Menu__display_all_menu_commands_02():
    r'''Hidden menu persists after junk.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = '? asdf q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - example scores',
        'Score manager - example scores',
        'Score manager - example scores',
        ]
    assert score_manager._transcript.titles == titles


def test_Menu__display_all_menu_commands_03():
    r'''Hidden menu persists after 'LilyPond log view.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = '? ll q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - example scores',
        'Score manager - example scores',
        'Score manager - example scores',
        ]
    assert score_manager._transcript.titles == titles


def test_Menu__display_all_menu_commands_04():
    r'''Hidden menu is available when managing score package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score ? q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles