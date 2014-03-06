# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_short_instrument_name_markup_01():
    r'''Quit, back & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation hornist horn sm q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (13,)

    string = 'red~example~score setup instrumentation'
    string += ' hornist horn sm b q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (15, (10, 13))

    string = 'red~example~score setup instrumentation'
    string += ' hornist horn sm h q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (15, (0, 13))
