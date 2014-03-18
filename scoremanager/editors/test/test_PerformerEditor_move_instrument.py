# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerEditor_move_instrument_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'étude~example~score setup instrumentation flutist mv q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (11,)

    input_ = 'étude~example~score setup instrumentation flutist mv b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13, (8, 11))

    input_ = 'étude~example~score setup instrumentation flutist mv h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13, (0, 11))

    input_ = 'étude~example~score setup instrumentation flutist mv s q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13, (2, 11))

    input_ = 'étude~example~score setup instrumentation'
    input_ += ' flutist mv foo q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13,)


def test_PerformerEditor_move_instrument_02():
    r'''Add two instruments. Move them.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.PerformerEditor(session=session)
    input_ = 'add 1 add 2 mv 1 2 q'
    editor._run(pending_user_input=input_)
    assert editor.target == instrumenttools.Performer(
        instruments=[
            instrumenttools.AltoVoice(), 
            instrumenttools.Accordion(),
            ],
        )
