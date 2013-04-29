from abjad import *
from experimental import *


def test_InstrumentEditor_short_instrument_name_markup_01():
    '''Quit, back & home all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist horn sm q')
    assert score_manager.transcript_signature == (13,)

    score_manager.run(user_input='example~score~i setup performers hornist horn sm b q')
    assert score_manager.transcript_signature == (15, (10, 13))

    score_manager.run(user_input='example~score~i setup performers hornist horn sm home q')
    assert score_manager.transcript_signature == (15, (0, 13))
