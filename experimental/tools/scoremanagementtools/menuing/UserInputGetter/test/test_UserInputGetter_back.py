from experimental import *


def test_UserInputGetter_back_01():

    score_manager = scoremanagementtools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers move b q')
    assert score_manager.ts == (11, (6, 9))
