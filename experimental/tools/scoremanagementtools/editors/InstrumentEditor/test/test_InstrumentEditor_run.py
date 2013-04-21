from abjad import *
from experimental import *


def test_InstrumentEditor_run_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagementtools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist horn q')
    assert score_manager.ts == (12,)

    score_manager = scoremanagementtools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist horn b q')
    assert score_manager.ts == (14, (8, 12))

    score_manager = scoremanagementtools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist horn home q')
    assert score_manager.ts == (14, (0, 12))

    score_manager = scoremanagementtools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist horn score q')
    assert score_manager.ts == (14, (2, 12))

    score_manager = scoremanagementtools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist horn foo q')
    assert score_manager.ts == (14, (10, 12))
