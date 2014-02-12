# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentationEditor_run_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation q')
    assert score_manager.session.io_transcript.signature == (8,)

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation b q')
    assert score_manager.session.io_transcript.signature == (10, (4, 8))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation home q')
    assert score_manager.session.io_transcript.signature == (10, (0, 8))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation score q')
    assert score_manager.session.io_transcript.signature == (10, (2, 8))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation foo q')
    assert score_manager.session.io_transcript.signature == (10, (6, 8))
