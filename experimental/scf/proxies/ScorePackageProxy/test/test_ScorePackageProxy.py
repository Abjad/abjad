# -*- encoding: utf-8 -*-
import scf


def test_ScorePackageProxy_01():
    '''Main menu.
    '''

    example_score_1 = scf.proxies.ScorePackageProxy('example_score_1')
    example_score_1.run(user_input='q')

    assert example_score_1.transcript[-2] == \
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

    example_score_1 = scf.proxies.ScorePackageProxy('example_score_1')
    example_score_1.session.user_input = 'q'
    example_score_1.manage_tags()
    assert example_score_1.ts == (2,)


def test_ScorePackageProxy_03():
    '''Add and delete tag interactively.
    '''

    example_score_1 = scf.proxies.ScorePackageProxy('example_score_1')
    example_score_1.session.user_input = 'add foo bar q'
    example_score_1.manage_tags()
    assert example_score_1.get_tag('foo') == 'bar'

    example_score_1 = scf.proxies.ScorePackageProxy('example_score_1')
    example_score_1.session.user_input = 'del foo q'
    example_score_1.manage_tags()
    assert example_score_1.get_tag('foo') is None


def test_ScorePackageProxy_04():
    '''User 'studio' input results in return to studio main menu.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input="example~score studio q")

    assert studio.ts == (6, (0, 4))
    assert studio.transcript[0][0] == 'Studio - active scores'
    assert studio.transcript[2][0] == 'Example Score I (2013)'
    assert studio.transcript[4][0] == 'Studio - active scores'


def test_ScorePackageProxy_05():
    '''User 'studio' input terminates execution (when score not managed from studio).
    '''

    example_score_1 = scf.proxies.ScorePackageProxy('example_score_1')
    example_score_1.run(user_input='studio')

    assert example_score_1.ts == (2,)
    assert example_score_1.transcript[0][0] == "Example Score I (2013)"
    assert example_score_1.transcript[1][0] == 'SCF> studio'


def test_ScorePackageProxy_06():
    '''User 'b' input returns to studio main menu.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='example~score b q')

    assert studio.ts == (6, (0, 4))
    assert studio.transcript[0][0] == 'Studio - active scores'
    assert studio.transcript[2][0] == 'Example Score I (2013)'
    assert studio.transcript[4][0] == 'Studio - active scores'


def test_ScorePackageProxy_07():
    '''Shared session.
    '''

    spp = scf.proxies.ScorePackageProxy('example_score_1')

    assert spp.session is spp.dist_proxy.session
    assert spp.session is spp.etc_proxy.session
    assert spp.session is spp.exg_proxy.session
    assert spp.session is spp.mus_proxy.session
    assert spp.session is spp.chunk_wrangler.session
    assert spp.session is spp.material_package_wrangler.session
    assert spp.session is spp.material_package_maker_wrangler.session
