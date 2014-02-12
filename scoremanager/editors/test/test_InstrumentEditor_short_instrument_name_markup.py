# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_short_instrument_name_markup_01():
    r'''Quit, back & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score score~setup instrumentation hornist horn sm q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (13,)

    string = 'red~example~score score~setup instrumentation'
    string += ' hornist horn sm b q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (15, (10, 13))

    string = 'red~example~score score~setup instrumentation'
    string += ' hornist horn sm home q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (15, (0, 13))
