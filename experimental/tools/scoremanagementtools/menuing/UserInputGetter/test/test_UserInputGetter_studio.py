from experimental import *


def test_UserInputGetter_studio_01():

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='example~score~i setup performers move stu q')
    assert studio.ts == (11, (0, 9))
