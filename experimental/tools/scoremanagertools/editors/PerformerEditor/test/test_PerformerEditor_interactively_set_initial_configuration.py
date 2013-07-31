# -*- encoding: utf-8 -*-
from experimental import *


def test_PerformerEditor_interactively_set_initial_configuration_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers add accordionist q')
    assert score_manager.session.io_transcript.signature == (12,)

    score_manager._run(pending_user_input='red~example~score setup performers add accodionist b q')
    assert score_manager.session.io_transcript.signature == (14, (6, 12), (8, 10))

    score_manager._run(pending_user_input='red~example~score setup performers add accordionist home q')
    assert score_manager.session.io_transcript.signature == (14, (0, 12))

    score_manager._run(pending_user_input='red~example~score setup performers add accordionist score q')
    assert score_manager.session.io_transcript.signature == (14, (2, 12))

    score_manager._run(pending_user_input='red~example~score setup performers add accordionist foo q')
    assert score_manager.session.io_transcript.signature == (14, (10, 12))
