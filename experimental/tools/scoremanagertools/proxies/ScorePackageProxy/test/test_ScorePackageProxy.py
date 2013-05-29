# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageProxy_01():
    '''Main menu.
    '''

    red_example_score = scoremanagertools.proxies.ScorePackageProxy(
        'scoremanagertools.built_in_scores.red_example_score')
    red_example_score._run(user_input='q')

    assert red_example_score._session.transcript[-2][1] == \
    ['Red Example Score (2013)',
      '',
      '     segments (h)',
      '     materials (m)',
      '     specifiers (f)',
      '     setup (s)',
      '']


def test_ScorePackageProxy_02():
    '''Manage tags menu.
    '''

    red_example_score = scoremanagertools.proxies.ScorePackageProxy(
        'scoremanagertools.built_in_scores.red_example_score')
    red_example_score._session.user_input = 'q'
    red_example_score.manage_tags()
    assert red_example_score._session.transcript.signature == (2,)


def test_ScorePackageProxy_03():
    '''Add and delete tag interactively.
    '''

    red_example_score = scoremanagertools.proxies.ScorePackageProxy(
        'scoremanagertools.built_in_scores.red_example_score')
    red_example_score._session.user_input = 'add foo bar q'
    red_example_score.manage_tags()
    assert red_example_score.get_tag('foo') == 'bar'

    red_example_score = scoremanagertools.proxies.ScorePackageProxy(
        'scoremanagertools.built_in_scores.red_example_score')
    red_example_score._session.user_input = 'del foo q'
    red_example_score.manage_tags()
    assert red_example_score.get_tag('foo') is None


def test_ScorePackageProxy_04():
    '''User 'home' input results in return home.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input="red~example~score home q")

    assert score_manager._session.transcript.signature == (6, (0, 4))
    assert score_manager._session.transcript[0][1][0] == 'Score manager - active scores'
    assert score_manager._session.transcript[2][1][0] == 'Red Example Score (2013)'
    assert score_manager._session.transcript[4][1][0] == 'Score manager - active scores'


def test_ScorePackageProxy_05():
    '''User 'home' input terminates execution (when score not managed from home).
    '''

    red_example_score = scoremanagertools.proxies.ScorePackageProxy(
        'scoremanagertools.built_in_scores.red_example_score')
    red_example_score._run(user_input='home')

    assert red_example_score._session.transcript.signature == (2,)
    assert red_example_score._session.transcript[0][1][0] == "Red Example Score (2013)"
    assert red_example_score._session.transcript[1][1][0] == '> home'


def test_ScorePackageProxy_06():
    '''User 'b' input returns home.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input='red~example~score b q')

    assert score_manager._session.transcript.signature == (6, (0, 4))
    assert score_manager._session.transcript[0][1][0] == 'Score manager - active scores'
    assert score_manager._session.transcript[2][1][0] == 'Red Example Score (2013)'
    assert score_manager._session.transcript[4][1][0] == 'Score manager - active scores'


def test_ScorePackageProxy_07():
    '''Shared session.
    '''

    spp = scoremanagertools.proxies.ScorePackageProxy(
        'scoremanagertools.built_in_scores.red_example_score')

    assert spp._session is spp.distribution_proxy._session
    assert spp._session is spp.exergue_directory_proxy._session
    assert spp._session is spp.music_proxy._session
    assert spp._session is spp.segment_wrangler._session
    assert spp._session is spp.material_package_wrangler._session
    assert spp._session is spp.material_package_maker_wrangler._session
