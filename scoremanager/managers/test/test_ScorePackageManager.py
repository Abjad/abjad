# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_ScorePackageManager_01():
    r'''Main menu.
    '''

    string = 'scoremanager.scores.red_example_score'
    filesystem_path = os.path.join(
        configuration.abjad_score_packages_directory_path,
        'red_example_score',
        )
    red_example_score = scoremanager.managers.ScorePackageManager(
        filesystem_path=filesystem_path)
    red_example_score._run(pending_user_input='q')

    assert red_example_score._transcript.last_menu_lines == \
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

    assert score_manager._transcript.signature == (6, (0, 4))
    string = 'Score manager - example scores'
    assert score_manager._transcript[0].title == string
    string = 'Red Example Score (2013)'
    assert score_manager._transcript[2].title == string
    string = 'Score manager - example scores'
    assert score_manager._transcript[4].title == string


def test_ScorePackageManager_03():
    r'''User 'home' input terminates execution (when score not managed 
    from home).
    '''

    string = 'scoremanager.scores.red_example_score'
    filesystem_path = os.path.join(
        configuration.abjad_score_packages_directory_path,
        'red_example_score',
        )
    red_example_score = scoremanager.managers.ScorePackageManager(
        filesystem_path=filesystem_path)
    red_example_score._run(pending_user_input='h')

    assert red_example_score._transcript.signature == (2,)
    string = "Red Example Score (2013)"
    assert red_example_score._transcript[0].title == string
    assert red_example_score._transcript[1].title == '> h'


def test_ScorePackageManager_04():
    r'''User 'b' input returns home.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score b q')

    assert score_manager._transcript.signature == (6, (0, 4))
    string = 'Score manager - example scores'
    assert score_manager._transcript[0].title == string
    string = 'Red Example Score (2013)'
    assert score_manager._transcript[2].title == string
    string = 'Score manager - example scores'
    assert score_manager._transcript[4].title == string


def test_ScorePackageManager_05():
    r'''Shared _session.
    '''

    string = 'scoremanager.scores.red_example_score'
    filesystem_path = os.path.join(
        configuration.abjad_score_packages_directory_path,
        'red_example_score',
        )
    manager = scoremanager.managers.ScorePackageManager(
        filesystem_path=filesystem_path)

    assert manager._session is manager._distribution_directory_manager._session
    assert manager._session is manager._build_directory_manager._session
    assert manager._session is manager._segment_package_wrangler._session
    assert manager._session is manager._material_package_wrangler._session
    assert manager._session is manager._material_package_manager_wrangler._session
