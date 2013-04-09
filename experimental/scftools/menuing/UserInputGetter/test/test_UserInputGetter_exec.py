import scftools


def test_UserInputGetter_exec_01():

    studio = scftools.studio.Studio()
    studio.run(user_input='1 setup performers move exec 2**30 q')
    assert studio.ts == (12,)
