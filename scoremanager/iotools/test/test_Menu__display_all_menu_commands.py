# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu__display_all_menu_commands_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = '? q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    assert 'commands - all' in contents
    assert 'library - build files' in contents
    assert 'scores - new' in contents


def test_Menu__display_all_menu_commands_02():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = '? q'
    score_manager._run(pending_user_input=input_)

    title = 'Score manager - example scores'
    assert score_manager._transcript.last_title == title


def test_Menu__display_all_menu_commands_03():
    r'''Hidden menu persists after junk.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = '? asdf q'
    score_manager._run(pending_user_input=input_)

    title_1 = 'Score manager - example scores'
    title_2 = 'Score manager - example scores'
    transcript = score_manager._transcript

    assert transcript.system_display_entries[-1].title == title_1
    assert transcript.system_display_entries[-2].title == title_2


def test_Menu__display_all_menu_commands_04():
    r'''Hidden menu persists after 'LilyPond log view.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = '? llro q'
    score_manager._run(pending_user_input=input_)

    title_2 = 'Score manager - example scores'
    title_1 = 'Score manager - example scores'
    transcript = score_manager._transcript

    assert transcript.system_display_entries[-2].title == title_2
    assert transcript.system_display_entries[-1].title == title_1


def test_Menu__display_all_menu_commands_05():
    r'''Hidden menu is available when managing score package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score ? q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    title = 'Red Example Score (2013)'
    assert transcript.system_display_entries[-1].title == title


def test_Menu__display_all_menu_commands_06():
    r'''Hidden menu persists after running doctest.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score ? pyd default q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    title = 'Red Example Score (2013)'
    assert transcript.last_title == title


def test_Menu__display_all_menu_commands_07():
    r'''Hidden menu persists after running py.test.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score ? pyt default q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    title = 'Red Example Score (2013)'
    assert transcript.last_title == title


def test_Menu__display_all_menu_commands_08():
    r'''Hidden menu persists after Python prompt.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score ? pyi 2**38 redraw q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    title = 'Red Example Score (2013)'
    assert transcript.last_title == title


def test_Menu__display_all_menu_commands_09():
    r'''Hidden menu persists after adding assets to repository.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score ? rad q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    title = 'Red Example Score (2013)'
    assert transcript.last_title == title


def test_Menu__display_all_menu_commands_10():
    r'''Hidden menu persists after commiting assets to repository.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score ? rci q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    title = 'Red Example Score (2013)'
    assert transcript.last_title == title


def test_Menu__display_all_menu_commands_11():
    r'''Hidden menu persists after displaying repository status.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score ? rst default q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    title = 'Red Example Score (2013)'
    assert transcript.last_title == title


def test_Menu__display_all_menu_commands_12():
    r'''Hidden menu persists after updating from repository.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score ? rup q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    title = 'Red Example Score (2013)'
    assert transcript.last_title == title


def test_Menu__display_all_menu_commands_13():
    r'''Hidden menu persists after displaying session variables.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score ? o default q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    title = 'Red Example Score (2013)'
    assert transcript.last_title == title


def test_Menu__display_all_menu_commands_14():
    r'''Hidden menu persists after showing source code location.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score ? scl redraw q'
    score_manager._run(pending_user_input=input_)
    transcript = score_manager._transcript

    title = 'Red Example Score (2013)'
    assert transcript.last_title == title