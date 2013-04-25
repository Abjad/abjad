# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageProxy_edit_forces_tagline_interactively_01():
    '''Quit, back, score & home all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup tagline q')
    assert score_manager.ts == (7,)

    score_manager.run(user_input='example~score~i setup tagline b q')
    assert score_manager.ts == (9, (4, 7))

    score_manager.run(user_input='example~score~i setup tagline score q')
    assert score_manager.ts == (9, (2, 7))

    score_manager.run(user_input='example~score~i setup tagline home q')
    assert score_manager.ts == (9, (0, 7))


def test_ScorePackageProxy_edit_forces_tagline_interactively_02():

    try:
        score_manager = scoremanagertools.scoremanager.ScoreManager()
        score_manager.run(user_input='example~score~i setup tagline for~foo~bar q')
        example_score_1 = scoremanagertools.proxies.ScorePackageProxy('example_score_1')
        assert example_score_1.forces_tagline == 'for foo bar'
    finally:
        score_manager.run(user_input='example~score~i setup tagline for~six~players q')
        example_score_1 = scoremanagertools.proxies.ScorePackageProxy('example_score_1')
        assert example_score_1.forces_tagline == 'for six players'
