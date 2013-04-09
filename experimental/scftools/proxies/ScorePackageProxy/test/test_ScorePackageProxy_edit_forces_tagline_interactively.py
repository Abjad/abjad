# -*- encoding: utf-8 -*-
import scftools


def test_ScorePackageProxy_edit_forces_tagline_interactively_01():
    '''Quit, back, score & studio all work.
    '''

    studio = scftools.studio.Studio()
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
        studio = scftools.studio.Studio()
        studio.run(user_input='example~score setup tagline for~foo~bar q')
        example_score_1 = scftools.proxies.ScorePackageProxy('example_score_1')
        assert example_score_1.forces_tagline == 'for foo bar'
    finally:
        studio.run(user_input='example~score setup tagline for~six~players q')
        example_score_1 = scftools.proxies.ScorePackageProxy('example_score_1')
        assert example_score_1.forces_tagline == 'for six players'
