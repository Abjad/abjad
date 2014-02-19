# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerEditor_run_01():
    r'''Quit, back, home and junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation hornist q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (10,)

    string = 'red~example~score setup instrumentation hornist b q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (12, (6, 10))

    string = 'red~example~score setup instrumentation hornist h q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (12, (0, 10))

    string = 'red~example~score setup instrumentation hornist foo q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (12, (8, 10))
