from experimental import *


def test_PerformerEditor_run_01():
    '''Quit, back, home and junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist q')
    assert score_manager.ts == (10,)

    score_manager.run(user_input='example~score~i setup performers hornist b q')
    assert score_manager.ts == (12, (6, 10))

    score_manager.run(user_input='example~score~i setup performers hornist home q')
    assert score_manager.ts == (12, (0, 10))

    score_manager.run(user_input='example~score~i setup performers hornist foo q')
    assert score_manager.ts == (12, (8, 10))
