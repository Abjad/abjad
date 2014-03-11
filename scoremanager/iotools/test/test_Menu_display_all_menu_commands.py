# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_Menu_display_all_menu_commands_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='n q', is_test=True)

    string = 'Score manager - example scores - all commands'
    assert score_manager._transcript.last_title == string


def test_Menu_display_all_menu_commands_02():
    r'''Hidden menu persists after junk.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='n asdf q', is_test=True)

    string_1 = 'Score manager - example scores - all commands'
    string_2 = 'Score manager - example scores'
    transcript = score_manager._transcript

    assert transcript.system_display_entries[-1].title == string_2
    assert transcript.system_display_entries[-2].title == string_1


def test_Menu_display_all_menu_commands_03():
    r'''Hidden menu persists after 'LilyPond log view.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='n lvl q', is_test=True)

    string_2 = 'Score manager - example scores - all commands'
    string_1 = 'Score manager - example scores'
    transcript = score_manager._transcript

    assert transcript.system_display_entries[-2].title == string_2
    assert transcript.system_display_entries[-1].title == string_1


def test_Menu_display_all_menu_commands_04():
    r'''Hidden menu is available when managing score package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013) - all commands'
    transcript = score_manager._transcript
    assert transcript.system_display_entries[-1].title == string


def test_Menu_display_all_menu_commands_05():
    r'''Hidden menu persists after running doctest.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n pyd default q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013)'
    transcript = score_manager._transcript
    assert transcript.last_title == string


def test_Menu_display_all_menu_commands_06():
    r'''Hidden menu persists after running py.test.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n pyt default q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013)'
    transcript = score_manager._transcript
    assert transcript.last_title == string


def test_Menu_display_all_menu_commands_07():
    r'''Hidden menu persists after Python prompt.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n pyi 2**38 redraw q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013)'
    transcript = score_manager._transcript
    assert transcript.last_title == string


def test_Menu_display_all_menu_commands_08():
    r'''Hidden menu persists after adding assets to repository.
    '''
    pytest.skip('make me testable')

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n radd q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013) - all commands'
    transcript = score_manager._transcript
    assert transcript.last_title == string


def test_Menu_display_all_menu_commands_09():
    r'''Hidden menu persists after commiting assets to repository.
    '''
    pytest.skip('make me testable')

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n rci q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013) - all commands'
    transcript = score_manager._transcript
    assert transcript.last_title == string


def test_Menu_display_all_menu_commands_10():
    r'''Hidden menu persists after displaying repository status.
    '''
    pytest.skip('make me work')

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n rst q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013) - all commands'
    transcript = score_manager._transcript
    assert transcript.last_title == string


def test_Menu_display_all_menu_commands_11():
    r'''Hidden menu persists after updating from repository.
    '''
    pytest.skip('make me testable')

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n rup q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013) - all commands'
    transcript = score_manager._transcript
    assert transcript.last_title == string


def test_Menu_display_all_menu_commands_12():
    r'''Hidden menu persists after displaying session variables.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n o default q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013)'
    transcript = score_manager._transcript
    assert transcript.last_title == string


def test_Menu_display_all_menu_commands_13():
    r'''Hidden menu persists after turning on source code tracking.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n sct redraw q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013)'
    transcript = score_manager._transcript
    assert transcript.last_title == string


def test_Menu_display_all_menu_commands_14():
    r'''Hidden menu persists after showing source code location.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n sct scl redraw q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013)'
    transcript = score_manager._transcript
    assert transcript.last_title == string


def test_Menu_display_all_menu_commands_15():
    r'''Hidden menu persists after editing source code.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score n sct sce q'
    score_manager._run(pending_user_input=string, is_test=True)

    string = 'Red Example Score (2013)'
    transcript = score_manager._transcript
    assert transcript.last_title == string
    assert score_manager._session.attempted_to_open_file
