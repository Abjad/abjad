# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentationEditor__run_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (8,)

    input_ = 'red~example~score setup instrumentation b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (10, (4, 8))

    input_ = 'red~example~score setup instrumentation h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (10, (0, 8))

    input_ = 'red~example~score setup instrumentation s q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (10, (2, 8))

    input_ = 'red~example~score setup instrumentation foo q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (10, (6, 8))
