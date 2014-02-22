# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageManager_01():
    r'''Main menu.
    '''

    string = 'scoremanager.scorepackages.red_example_score'
    red_example_score = scoremanager.managers.ScorePackageManager(string)
    red_example_score._run(pending_user_input='q')

    assert red_example_score._session.transcript.last_menu_lines == \
    ['Red Example Score (2013)',
      '',
      '     build (u)',
      '     makers (k)',
      '     materials (m)',
      '     segments (g)',
      '     setup (p)',
      '     templates (t)',
      '     stylesheets (y)',
      '']


def test_ScorePackageManager_02():
    r'''User 'home' input results in return home.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input="red~example~score h q")

    assert score_manager._session.transcript.signature == (6, (0, 4))
    string = 'Score manager - example scores'
    assert score_manager._session.transcript[0].title == string
    string = 'Red Example Score (2013)'
    assert score_manager._session.transcript[2].title == string
    string = 'Score manager - example scores'
    assert score_manager._session.transcript[4].title == string


def test_ScorePackageManager_03():
    r'''User 'home' input terminates execution (when score not managed 
    from home).
    '''

    string = 'scoremanager.scorepackages.red_example_score'
    red_example_score = scoremanager.managers.ScorePackageManager(string)
    red_example_score._run(pending_user_input='h')

    assert red_example_score._session.transcript.signature == (2,)
    string = "Red Example Score (2013)"
    assert red_example_score._session.transcript[0].title == string
    assert red_example_score._session.transcript[1].title == '> h'


def test_ScorePackageManager_04():
    r'''User 'b' input returns home.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score b q')

    assert score_manager._session.transcript.signature == (6, (0, 4))
    string = 'Score manager - example scores'
    assert score_manager._session.transcript[0].title == string
    string = 'Red Example Score (2013)'
    assert score_manager._session.transcript[2].title == string
    string = 'Score manager - example scores'
    assert score_manager._session.transcript[4].title == string


def test_ScorePackageManager_05():
    r'''Shared _session.
    '''

    string = 'scoremanager.scorepackages.red_example_score'
    manager = scoremanager.managers.ScorePackageManager(string)

    assert manager._session is manager._distribution_directory_manager._session
    assert manager._session is manager._build_directory_manager._session
    assert manager._session is manager._segment_package_wrangler._session
    assert manager._session is manager._material_package_wrangler._session
    assert manager._session is manager._material_package_manager_wrangler._session
