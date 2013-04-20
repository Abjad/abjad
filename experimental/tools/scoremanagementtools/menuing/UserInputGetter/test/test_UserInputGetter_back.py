from experimental import *


def test_UserInputGetter_back_01():

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i setup performers move b q')
    assert studio.ts == (11, (6, 9))
