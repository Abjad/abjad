# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageManager_01():
    r'''Main menu.
    '''

    red_example_score = scoremanagertools.proxies.ScorePackageManager(
        'scoremanagertools.scorepackages.red_example_score')
    red_example_score._run(pending_user_input='q')

    assert red_example_score.session.io_transcript[-2][1] == \
    ['Red Example Score (2013)',
      '',
      '     build directory (u)',
      '     materials (m)',
      '     score segments (g)',
      '     score setup (s)',
      '     score templates (t)',
      '     stylesheets (y)',
      '']


def test_ScorePackageManager_02():
    r'''Manage tags menu.
    '''

    red_example_score = scoremanagertools.proxies.ScorePackageManager(
        'scoremanagertools.scorepackages.red_example_score')
    red_example_score.session.pending_user_input = 'q'
    red_example_score.manage_tags()
    assert red_example_score.session.io_transcript.signature == (2,)


def test_ScorePackageManager_03():
    r'''Add and delete tag interactively.
    '''

    red_example_score = scoremanagertools.proxies.ScorePackageManager(
        'scoremanagertools.scorepackages.red_example_score')
    red_example_score.session.pending_user_input = 'add foo bar q'
    red_example_score.manage_tags()
    assert red_example_score.get_tag('foo') == 'bar'

    red_example_score = scoremanagertools.proxies.ScorePackageManager(
        'scoremanagertools.scorepackages.red_example_score')
    red_example_score.session.pending_user_input = 'del foo q'
    red_example_score.manage_tags()
    assert red_example_score.get_tag('foo') is None


def test_ScorePackageManager_04():
    r'''User 'home' input results in return home.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input="red~example~score home q")

    assert score_manager.session.io_transcript.signature == (6, (0, 4))
    assert score_manager.session.io_transcript[0][1][0] == 'Score manager - active scores'
    assert score_manager.session.io_transcript[2][1][0] == 'Red Example Score (2013)'
    assert score_manager.session.io_transcript[4][1][0] == 'Score manager - active scores'


def test_ScorePackageManager_05():
    r'''User 'home' input terminates execution (when score not managed from home).
    '''

    red_example_score = scoremanagertools.proxies.ScorePackageManager(
        'scoremanagertools.scorepackages.red_example_score')
    red_example_score._run(pending_user_input='home')

    assert red_example_score.session.io_transcript.signature == (2,)
    assert red_example_score.session.io_transcript[0][1][0] == "Red Example Score (2013)"
    assert red_example_score.session.io_transcript[1][1][0] == '> home'


def test_ScorePackageManager_06():
    r'''User 'b' input returns home.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score b q')

    assert score_manager.session.io_transcript.signature == (6, (0, 4))
    assert score_manager.session.io_transcript[0][1][0] == 'Score manager - active scores'
    assert score_manager.session.io_transcript[2][1][0] == 'Red Example Score (2013)'
    assert score_manager.session.io_transcript[4][1][0] == 'Score manager - active scores'


def test_ScorePackageManager_07():
    r'''Shared session.
    '''

    spp = scoremanagertools.proxies.ScorePackageManager(
        'scoremanagertools.scorepackages.red_example_score')

    assert spp.session is spp.distribution_directory_manager.session
    assert spp.session is spp.build_directory_manager.session
    assert spp.session is spp.segment_wrangler.session
    assert spp.session is spp.material_package_wrangler.session
    assert spp.session is spp.material_package_maker_wrangler.session
