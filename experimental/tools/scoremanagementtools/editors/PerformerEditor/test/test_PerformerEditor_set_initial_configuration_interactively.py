from experimental import *


def test_PerformerEditor_set_initial_configuration_interactively_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i setup performers add accordionist q')
    assert studio.ts == (12,)

    studio.run(user_input='example~score~i setup performers add accodionist b q')
    assert studio.ts == (14, (6, 12), (8, 10))

    studio.run(user_input='example~score~i setup performers add accordionist studio q')
    assert studio.ts == (14, (0, 12))

    studio.run(user_input='example~score~i setup performers add accordionist score q')
    assert studio.ts == (14, (2, 12))

    studio.run(user_input='example~score~i setup performers add accordionist foo q')
    assert studio.ts == (14, (10, 12))
