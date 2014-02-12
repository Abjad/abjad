# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentEditor_run_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn q')
    assert score_manager.session.io_transcript.signature == (12,)

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn b q')
    assert score_manager.session.io_transcript.signature == (14, (8, 12))

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn home q')
    assert score_manager.session.io_transcript.signature == (14, (0, 12))

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn score q')
    assert score_manager.session.io_transcript.signature == (14, (2, 12))

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn foo q')
    assert score_manager.session.io_transcript.signature == (14, (10, 12))
