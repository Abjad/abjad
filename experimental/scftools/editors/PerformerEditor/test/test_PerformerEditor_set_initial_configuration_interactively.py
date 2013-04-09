import scftools


def test_PerformerEditor_set_initial_configuration_interactively_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='1 setup performers add 1 q')
    assert studio.ts == (12, (1, 9))

    studio.run(user_input='1 setup performers add 1 b q')
    assert studio.ts == (14, (1, 9), (8, 12))

    studio.run(user_input='1 setup performers add 1 studio q')
    assert studio.ts == (14, (0, 12), (1, 9))

    studio.run(user_input='1 setup performers add 1 score q')
    assert studio.ts == (14, (1, 9), (2, 12))

    studio.run(user_input='1 setup performers add 1 foo q')
    assert studio.ts == (14, (1, 9), (10, 12))
