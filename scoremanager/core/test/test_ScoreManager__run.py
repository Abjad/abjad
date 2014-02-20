# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager__run_01():
    r'''Quit, home & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='q')
    assert score_manager.session.io_transcript.signature == (2,)

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='h q')
    assert score_manager.session.io_transcript.signature == (4, (0, 2))

    score_manager._run(pending_user_input='foo q')
    assert score_manager.session.io_transcript.signature == (4, (0, 2))


def test_ScoreManager__run_02():
    r'''Score is handled correctly.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='s q')
    assert score_manager.session.io_transcript.signature == (4, (0, 2))


def test_ScoreManager__run_03():
    r'''Back is handled correctly.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='b q')
    assert score_manager.session.io_transcript.signature == (4, (0, 2))
