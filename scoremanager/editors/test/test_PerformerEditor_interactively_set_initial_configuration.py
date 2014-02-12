# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerEditor_interactively_set_initial_configuration_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation add accordionist q')
    assert score_manager.session.io_transcript.signature == (12,)

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation add accodionist b q')
    assert score_manager.session.io_transcript.signature == (14, (6, 12), (8, 10))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation add accordionist home q')
    assert score_manager.session.io_transcript.signature == (14, (0, 12))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation add accordionist score q')
    assert score_manager.session.io_transcript.signature == (14, (2, 12))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation add accordionist foo q')
    assert score_manager.session.io_transcript.signature == (14, (10, 12))
