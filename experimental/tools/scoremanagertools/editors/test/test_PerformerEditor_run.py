# -*- encoding: utf-8 -*-
from experimental import *


def test_PerformerEditor_run_01():
    r'''Quit, back, home and junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist q')
    assert score_manager.session.io_transcript.signature == (10,)

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist b q')
    assert score_manager.session.io_transcript.signature == (12, (6, 10))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist home q')
    assert score_manager.session.io_transcript.signature == (12, (0, 10))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist foo q')
    assert score_manager.session.io_transcript.signature == (12, (8, 10))
