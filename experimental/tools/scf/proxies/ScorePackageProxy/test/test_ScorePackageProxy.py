# -*- encoding: utf-8 -*-
import scf


def test_ScorePackageProxy_01():
    '''Main menu.
    '''

    archipel = scf.proxies.ScorePackageProxy('archipel')
    archipel.run(user_input='q')

    assert archipel.transcript[-2] == \
    ["L'archipel du corps (2011)",
      '',
      '     chunks (h)',
      '     materials (m)',
      '     specifiers (f)',
      '     setup (s)',
      '']


def test_ScorePackageProxy_02():
    '''Manage tags menu.
    '''

    archipel = scf.proxies.ScorePackageProxy('archipel')
    archipel.session.user_input = 'q'
    archipel.manage_tags()
    assert archipel.ts == (2,)


def test_ScorePackageProxy_03():
    '''Add and delete tag interactively.
    '''

    archipel = scf.proxies.ScorePackageProxy('archipel')
    archipel.session.user_input = 'add foo bar q'
    archipel.manage_tags()
    assert archipel.get_tag('foo') == 'bar'

    archipel = scf.proxies.ScorePackageProxy('archipel')
    archipel.session.user_input = 'del foo q'
    archipel.manage_tags()
    assert archipel.get_tag('foo') is None


def test_ScorePackageProxy_04():
    '''User 'studio' input results in return to studio main menu.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input="l'arch studio q")

    assert studio.ts == (6, (0, 4))
    assert studio.transcript[0][0] == 'Studio - active scores'
    assert studio.transcript[2][0] == "L'archipel du corps (2011)"
    assert studio.transcript[4][0] == 'Studio - active scores'


def test_ScorePackageProxy_05():
    '''User 'studio' input terminates execution (when score not managed from studio).
    '''

    archipel = scf.proxies.ScorePackageProxy('archipel')
    archipel.run(user_input='studio')

    assert archipel.ts == (2,)
    assert archipel.transcript[0][0] == "L'archipel du corps (2011)"
    assert archipel.transcript[1][0] == 'SCF> studio'


def test_ScorePackageProxy_06():
    '''User 'b' input returns to studio main menu.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input="l'arch b q")

    assert studio.ts == (6, (0, 4))
    assert studio.transcript[0][0] == 'Studio - active scores'
    assert studio.transcript[2][0] == "L'archipel du corps (2011)"
    assert studio.transcript[4][0] == 'Studio - active scores'


def test_ScorePackageProxy_07():
    '''Shared session.
    '''

    spp = scf.proxies.ScorePackageProxy('archipel')

    assert spp.session is spp.dist_proxy.session
    assert spp.session is spp.etc_proxy.session
    assert spp.session is spp.exg_proxy.session
    assert spp.session is spp.mus_proxy.session
    assert spp.session is spp.chunk_wrangler.session
    assert spp.session is spp.material_package_wrangler.session
    assert spp.session is spp.material_package_maker_wrangler.session
