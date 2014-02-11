# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentEditor_short_instrument_name_markup_01():
    r'''Quit, back & home all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn sm q')
    assert score_manager.session.io_transcript.signature == (13,)

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn sm b q')
    assert score_manager.session.io_transcript.signature == (15, (10, 13))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn sm home q')
    assert score_manager.session.io_transcript.signature == (15, (0, 13))
