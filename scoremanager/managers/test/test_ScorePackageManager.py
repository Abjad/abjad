# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageManager_01():
    r'''Main menu.
    '''

    string = 'scoremanager.scorepackages.red_example_score'
    red_example_score = scoremanager.managers.ScorePackageManager(string)
    red_example_score._run(pending_user_input='q')

    assert red_example_score.session.io_transcript[-2][1] == \
    ['Red Example Score (2013)',
      '',
      '     build directory (u)',
      '     makers (k)',
      '     materials (m)',
      '     score segments (g)',
      '     score setup (s)',
      '     score templates (t)',
      '     stylesheets (y)',
      '']


def test_ScorePackageManager_02():
    r'''Manage metadata menu.
    '''

    string = 'scoremanager.scorepackages.red_example_score'
    red_example_score = scoremanager.managers.ScorePackageManager(string)
    red_example_score.session.pending_user_input = 'q'
    red_example_score.manage_metadata()
    assert red_example_score.session.io_transcript.signature == (2,)


def test_ScorePackageManager_03():
    r'''User 'home' input results in return home.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input="red~example~score home q")

    assert score_manager.session.io_transcript.signature == (6, (0, 4))
    string = 'Score manager - active scores'
    assert score_manager.session.io_transcript[0][1][0] == string
    string = 'Red Example Score (2013)'
    assert score_manager.session.io_transcript[2][1][0] == string
    string = 'Score manager - active scores'
    assert score_manager.session.io_transcript[4][1][0] == string


def test_ScorePackageManager_04():
    r'''User 'home' input terminates execution (when score not managed 
    from home).
    '''

    string = 'scoremanager.scorepackages.red_example_score'
    red_example_score = scoremanager.managers.ScorePackageManager(string)
    red_example_score._run(pending_user_input='home')

    assert red_example_score.session.io_transcript.signature == (2,)
    string = "Red Example Score (2013)"
    assert red_example_score.session.io_transcript[0][1][0] == string
    assert red_example_score.session.io_transcript[1][1][0] == '> home'


def test_ScorePackageManager_05():
    r'''User 'b' input returns home.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score b q')

    assert score_manager.session.io_transcript.signature == (6, (0, 4))
    string = 'Score manager - active scores'
    assert score_manager.session.io_transcript[0][1][0] == string
    string = 'Red Example Score (2013)'
    assert score_manager.session.io_transcript[2][1][0] == string
    string = 'Score manager - active scores'
    assert score_manager.session.io_transcript[4][1][0] == string


def test_ScorePackageManager_06():
    r'''Shared session.
    '''

    string = 'scoremanager.scorepackages.red_example_score'
    manager = scoremanager.managers.ScorePackageManager(string)

    assert manager.session is manager.distribution_directory_manager.session
    assert manager.session is manager.build_directory_manager.session
    assert manager.session is manager.segment_wrangler.session
    assert manager.session is manager.material_package_wrangler.session
    assert manager.session is manager.material_package_manager_wrangler.session
