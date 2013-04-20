from experimental import *


def test_UserInputGetter_exec_01():

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i setup performers move exec 2**30 q')
    assert studio.ts == (12,)
