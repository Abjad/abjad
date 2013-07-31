# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageProxy_interactively_edit_forces_tagline_01():
    r'''Quit, back, score & home all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup tagline q')
    assert score_manager.session.io_transcript.signature == (7,)

    score_manager._run(pending_user_input='red~example~score setup tagline b q')
    assert score_manager.session.io_transcript.signature == (9, (4, 7))

    score_manager._run(pending_user_input='red~example~score setup tagline score q')
    assert score_manager.session.io_transcript.signature == (9, (2, 7))

    score_manager._run(pending_user_input='red~example~score setup tagline home q')
    assert score_manager.session.io_transcript.signature == (9, (0, 7))


def test_ScorePackageProxy_interactively_edit_forces_tagline_02():

    try:
        score_manager = scoremanagertools.scoremanager.ScoreManager()
        score_manager._run(pending_user_input='red~example~score setup tagline for~foo~bar q')
        red_example_score = scoremanagertools.proxies.ScorePackageProxy(
            'scoremanagertools.scorepackages.red_example_score')
        assert red_example_score.forces_tagline == 'for foo bar'
    finally:
        score_manager._run(pending_user_input='red~example~score setup tagline for~six~players q')
        red_example_score = scoremanagertools.proxies.ScorePackageProxy(
            'scoremanagertools.scorepackages.red_example_score')
        assert red_example_score.forces_tagline == 'for six players'
