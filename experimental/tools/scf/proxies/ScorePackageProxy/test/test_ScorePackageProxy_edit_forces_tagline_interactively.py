# -*- encoding: utf-8 -*-
import scf


def test_ScorePackageProxy_edit_forces_tagline_interactively_01():
    '''Quit, back, score & studio all work.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='1 setup tagline q')
    assert studio.ts == (7,)

    studio.run(user_input='1 setup tagline b q')
    assert studio.ts == (9, (4, 7))

    studio.run(user_input='1 setup tagline score q')
    assert studio.ts == (9, (2, 7))

    studio.run(user_input='1 setup tagline studio q')
    assert studio.ts == (9, (0, 7))


def test_ScorePackageProxy_edit_forces_tagline_interactively_02():

    try:
        studio = scf.studio.Studio()
        studio.run(user_input='poeme setup tagline for~foo~bar q')
        recursif = scf.proxies.ScorePackageProxy('recursif')
        assert recursif.forces_tagline == 'for foo bar'
    finally:
        studio.run(user_input='poeme setup tagline for~64~pieces~of~percussion q')
        recursif = scf.proxies.ScorePackageProxy('recursif')
        assert recursif.forces_tagline == 'for 64 pieces of percussion'
