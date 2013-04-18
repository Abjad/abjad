# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageProxy_edit_forces_tagline_interactively_01():
    '''Quit, back, score & studio all work.
    '''

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='example~score~i setup tagline q')
    assert studio.ts == (7,)

    studio.run(user_input='example~score~i setup tagline b q')
    assert studio.ts == (9, (4, 7))

    studio.run(user_input='example~score~i setup tagline score q')
    assert studio.ts == (9, (2, 7))

    studio.run(user_input='example~score~i setup tagline studio q')
    assert studio.ts == (9, (0, 7))


def test_ScorePackageProxy_edit_forces_tagline_interactively_02():

    try:
        studio = scoremanagementtools.studio.Studio()
        studio.run(user_input='example~score~i setup tagline for~foo~bar q')
        example_score_1 = scoremanagementtools.proxies.ScorePackageProxy('example_score_1')
        assert example_score_1.forces_tagline == 'for foo bar'
    finally:
        studio.run(user_input='example~score~i setup tagline for~six~players q')
        example_score_1 = scoremanagementtools.proxies.ScorePackageProxy('example_score_1')
        assert example_score_1.forces_tagline == 'for six players'
