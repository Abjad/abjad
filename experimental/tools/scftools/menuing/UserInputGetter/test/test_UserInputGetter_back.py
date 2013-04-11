from experimental import *


def test_UserInputGetter_back_01():

    studio = scftools.studio.Studio()
    studio.run(user_input='1 setup performers move b q')
    assert studio.ts == (11, (6, 9))
