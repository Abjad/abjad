from experimental import *


def test_UserInputGetter_score_01():

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='1 setup performers move sco q')
    assert studio.ts == (11, (2, 9))
