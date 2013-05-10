from experimental import *


def test_PerformerEditor_set_initial_configuration_interactively_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input='example~score~i setup performers add accordionist q')
    assert score_manager._session.transcript.signature == (12,)

    score_manager._run(user_input='example~score~i setup performers add accodionist b q')
    assert score_manager._session.transcript.signature == (14, (6, 12), (8, 10))

    score_manager._run(user_input='example~score~i setup performers add accordionist home q')
    assert score_manager._session.transcript.signature == (14, (0, 12))

    score_manager._run(user_input='example~score~i setup performers add accordionist score q')
    assert score_manager._session.transcript.signature == (14, (2, 12))

    score_manager._run(user_input='example~score~i setup performers add accordionist foo q')
    assert score_manager._session.transcript.signature == (14, (10, 12))
