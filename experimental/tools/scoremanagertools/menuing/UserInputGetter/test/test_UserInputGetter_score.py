from experimental import *


def test_UserInputGetter_score_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers move sco q')
    assert score_manager.ts == (11, (2, 9))
