# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor__run_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist horn q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (12,)

    input_ = 'red~example~score setup instrumentation hornist horn b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (8, 12))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (0, 12))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn s q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (2, 12))

    input_ = 'red~example~score setup instrumentation hornist horn foo q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (10, 12))
