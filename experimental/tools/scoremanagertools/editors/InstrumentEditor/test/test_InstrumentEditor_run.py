from abjad import *
from experimental import *


def test_InstrumentEditor_run_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers hornist horn q')
    assert score_manager._session.transcript.signature == (12,)

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers hornist horn b q')
    assert score_manager._session.transcript.signature == (14, (8, 12))

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers hornist horn home q')
    assert score_manager._session.transcript.signature == (14, (0, 12))

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers hornist horn score q')
    assert score_manager._session.transcript.signature == (14, (2, 12))

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers hornist horn foo q')
    assert score_manager._session.transcript.signature == (14, (10, 12))
