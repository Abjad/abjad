from abjad import *
from experimental import *


def test_InstrumentEditor_short_instrument_name_markup_01():
    '''Quit, back & home all work.
    '''

    score_manager = scoremanagementtools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist horn sm q')
    assert score_manager.ts == (13,)

    score_manager.run(user_input='example~score~i setup performers hornist horn sm b q')
    assert score_manager.ts == (15, (10, 13))

    score_manager.run(user_input='example~score~i setup performers hornist horn sm home q')
    assert score_manager.ts == (15, (0, 13))
