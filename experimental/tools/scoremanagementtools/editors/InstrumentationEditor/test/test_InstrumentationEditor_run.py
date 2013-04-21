from experimental import *


def test_InstrumentationEditor_run_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagementtools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup perf q')
    assert score_manager.ts == (8,)

    score_manager.run(user_input='example~score~i setup perf b q')
    assert score_manager.ts == (10, (4, 8))

    score_manager.run(user_input='example~score~i setup perf home q')
    assert score_manager.ts == (10, (0, 8))

    score_manager.run(user_input='example~score~i setup perf score q')
    assert score_manager.ts == (10, (2, 8))

    score_manager.run(user_input='example~score~i setup perf foo q')
    assert score_manager.ts == (10, (6, 8))
