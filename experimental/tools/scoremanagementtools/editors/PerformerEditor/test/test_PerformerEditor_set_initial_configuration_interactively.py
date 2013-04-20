from experimental import *


def test_PerformerEditor_set_initial_configuration_interactively_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagementtools.studio.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers add accordionist q')
    assert score_manager.ts == (12,)

    score_manager.run(user_input='example~score~i setup performers add accodionist b q')
    assert score_manager.ts == (14, (6, 12), (8, 10))

    score_manager.run(user_input='example~score~i setup performers add accordionist home q')
    assert score_manager.ts == (14, (0, 12))

    score_manager.run(user_input='example~score~i setup performers add accordionist score q')
    assert score_manager.ts == (14, (2, 12))

    score_manager.run(user_input='example~score~i setup performers add accordionist foo q')
    assert score_manager.ts == (14, (10, 12))
