# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentationEditor_run_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (8,)

    string = 'red~example~score setup instrumentation b q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (10, (4, 8))

    string = 'red~example~score setup instrumentation h q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (10, (0, 8))

    string = 'red~example~score setup instrumentation s q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (10, (2, 8))

    string = 'red~example~score setup instrumentation foo q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (10, (6, 8))
