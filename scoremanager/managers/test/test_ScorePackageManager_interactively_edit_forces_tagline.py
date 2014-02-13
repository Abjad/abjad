# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageManager_interactively_edit_forces_tagline_01():
    r'''Quit, back, score & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score score~setup tagline q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (7,)

    string = 'red~example~score score~setup tagline b q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (9, (4, 7))

    string = 'red~example~score score~setup tagline score q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (9, (2, 7))

    string = 'red~example~score score~setup tagline home q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (9, (0, 7))


def test_ScorePackageManager_interactively_edit_forces_tagline_02():

    try:
        score_manager = scoremanager.core.ScoreManager()
        string = 'red~example~score score~setup tagline for~foo~bar q'
        score_manager._run(pending_user_input=string)
        path = 'scoremanager.scorepackages.red_example_score'
        manager = scoremanager.managers.ScorePackageManager(path)
        assert manager._get_metadatum('forces_tagline') == 'for foo bar'
    finally:
        string = 'red~example~score score~setup tagline for~six~players q'
        score_manager._run(pending_user_input=string)
        path = 'scoremanager.scorepackages.red_example_score'
        manager = scoremanager.managers.ScorePackageManager(path)
        assert manager._get_metadatum('forces_tagline') == 'for six players'
