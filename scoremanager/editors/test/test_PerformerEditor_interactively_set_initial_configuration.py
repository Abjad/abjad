# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerEditor_interactively_set_initial_configuration_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score score~setup instrumentation add accordionist q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (12,)

    string = 'red~example~score score~setup instrumentation'
    string += ' add accodionist b q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == \
        (14, (6, 12), (8, 10))

    string = 'red~example~score score~setup instrumentation'
    string += ' add accordionist home q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (14, (0, 12))

    string = 'red~example~score score~setup instrumentation'
    string += ' add accordionist score q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (14, (2, 12))

    string = 'red~example~score score~setup instrumentation'
    string += ' add accordionist foo q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (14, (10, 12))
