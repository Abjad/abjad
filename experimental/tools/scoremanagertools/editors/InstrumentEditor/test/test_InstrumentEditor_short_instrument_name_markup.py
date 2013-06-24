from abjad import *
from experimental import *


def test_InstrumentEditor_short_instrument_name_markup_01():
    '''Quit, back & home all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers hornist horn sm q')
    assert score_manager._session.transcript.signature == (13,)

    score_manager._run(pending_user_input='red~example~score setup performers hornist horn sm b q')
    assert score_manager._session.transcript.signature == (15, (10, 13))

    score_manager._run(pending_user_input='red~example~score setup performers hornist horn sm home q')
    assert score_manager._session.transcript.signature == (15, (0, 13))
