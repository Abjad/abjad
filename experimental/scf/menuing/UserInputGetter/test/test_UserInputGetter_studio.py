import scf


def test_UserInputGetter_studio_01():

    studio = scf.studio.Studio()
    studio.run(user_input='1 setup performers move stu q')
    assert studio.ts == (11, (0, 9))
