# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageProxy_01():
    '''Main menu.
    '''

    example_score_1 = scoremanagertools.proxies.ScorePackageProxy('example_score_1')
    example_score_1.run(user_input='q')

    assert example_score_1.session.transcript[-2] == \
    ['Example Score I (2013)',
      '',
      '     chunks (h)',
      '     materials (m)',
      '     specifiers (f)',
      '     setup (s)',
      '']


def test_ScorePackageProxy_02():
    '''Manage tags menu.
    '''

    example_score_1 = scoremanagertools.proxies.ScorePackageProxy('example_score_1')
    example_score_1.session.user_input = 'q'
    example_score_1.manage_tags()
    assert example_score_1.transcript_signature == (2,)


def test_ScorePackageProxy_03():
    '''Add and delete tag interactively.
    '''

    example_score_1 = scoremanagertools.proxies.ScorePackageProxy('example_score_1')
    example_score_1.session.user_input = 'add foo bar q'
    example_score_1.manage_tags()
    assert example_score_1.get_tag('foo') == 'bar'

    example_score_1 = scoremanagertools.proxies.ScorePackageProxy('example_score_1')
    example_score_1.session.user_input = 'del foo q'
    example_score_1.manage_tags()
    assert example_score_1.get_tag('foo') is None


def test_ScorePackageProxy_04():
    '''User 'home' input results in return home.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input="example~score~i home q")

    assert score_manager.transcript_signature == (6, (0, 4))
    assert score_manager.session.transcript[0][0] == 'Scores - active scores'
    assert score_manager.session.transcript[2][0] == 'Example Score I (2013)'
    assert score_manager.session.transcript[4][0] == 'Scores - active scores'


def test_ScorePackageProxy_05():
    '''User 'home' input terminates execution (when score not managed from home).
    '''

    example_score_1 = scoremanagertools.proxies.ScorePackageProxy('example_score_1')
    example_score_1.run(user_input='home')

    assert example_score_1.transcript_signature == (2,)
    assert example_score_1.session.transcript[0][0] == "Example Score I (2013)"
    assert example_score_1.session.transcript[1][0] == '> home'


def test_ScorePackageProxy_06():
    '''User 'b' input returns home.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i b q')

    assert score_manager.transcript_signature == (6, (0, 4))
    assert score_manager.session.transcript[0][0] == 'Scores - active scores'
    assert score_manager.session.transcript[2][0] == 'Example Score I (2013)'
    assert score_manager.session.transcript[4][0] == 'Scores - active scores'


def test_ScorePackageProxy_07():
    '''Shared session.
    '''

    spp = scoremanagertools.proxies.ScorePackageProxy('example_score_1')

    assert spp.session is spp.dist_proxy.session
    assert spp.session is spp.etc_proxy.session
    assert spp.session is spp.exg_proxy.session
    assert spp.session is spp.mus_proxy.session
    assert spp.session is spp.segment_wrangler.session
    assert spp.session is spp.material_package_wrangler.session
    assert spp.session is spp.material_package_maker_wrangler.session
