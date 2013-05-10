from experimental import *


def test_InstrumentEditor_instrument_name_markup_01():
    '''Quit, back & home all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist horn im q')
    assert score_manager._session.transcript.signature == (13,)

    score_manager.run(user_input='example~score~i setup performers hornist horn im b q')
    assert score_manager._session.transcript.signature == (15, (10, 13))

    score_manager.run(user_input='example~score~i setup performers hornist horn im home q')
    assert score_manager._session.transcript.signature == (15, (0, 13))
