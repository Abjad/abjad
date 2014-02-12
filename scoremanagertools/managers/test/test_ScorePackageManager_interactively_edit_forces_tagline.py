# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageManager_interactively_edit_forces_tagline_01():
    r'''Quit, back, score & home all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    user_input = 'red~example~score score~setup tagline q'
    score_manager._run(pending_user_input=user_input)
    assert score_manager.session.io_transcript.signature == (7,)

    user_input = 'red~example~score score~setup tagline b q'
    score_manager._run(pending_user_input=user_input)
    assert score_manager.session.io_transcript.signature == (9, (4, 7))

    user_input = 'red~example~score score~setup tagline score q'
    score_manager._run(pending_user_input=user_input)
    assert score_manager.session.io_transcript.signature == (9, (2, 7))

    user_input = 'red~example~score score~setup tagline home q'
    score_manager._run(pending_user_input=user_input)
    assert score_manager.session.io_transcript.signature == (9, (0, 7))


def test_ScorePackageManager_interactively_edit_forces_tagline_02():

    try:
        score_manager = scoremanagertools.scoremanager.ScoreManager()
        user_input = 'red~example~score score~setup tagline for~foo~bar q'
        score_manager._run(pending_user_input=user_input)
        path = 'scoremanagertools.scorepackages.red_example_score'
        manager = scoremanagertools.managers.ScorePackageManager(path)
        assert manager._get_metadata('forces_tagline') == 'for foo bar'
    finally:
        user_input = 'red~example~score score~setup tagline for~six~players q'
        score_manager._run(pending_user_input=user_input)
        path = 'scoremanagertools.scorepackages.red_example_score'
        manager = scoremanagertools.managers.ScorePackageManager(path)
        assert manager._get_metadata('forces_tagline') == 'for six players'
