# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerEditor_add_instruments_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist add q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (12,)

    input_ = 'red~example~score setup instrumentation hornist add b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (8, 12))

    input_ = 'red~example~score setup instrumentation hornist add h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (0, 12))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist add s q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (2, 12))

    input_ = 'red~example~score setup instrumentation hornist add foo q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (14, (10, 12))


def test_PerformerEditor_add_instruments_02():
    r'''Add two instruments.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.PerformerEditor(session=session)
    input_ = 'add 1 add 2 q'
    editor._run(pending_user_input=input_)
    assert editor.target == instrumenttools.Performer(
        instruments=[
            instrumenttools.Accordion(), 
            instrumenttools.AltoVoice(),
            ])


def test_PerformerEditor_add_instruments_03():
    r'''Range handling.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.PerformerEditor(session=session)
    input_ = 'add 1-2 q'
    editor._run(pending_user_input=input_)
    assert editor.target == instrumenttools.Performer(
        instruments=[
            instrumenttools.Accordion(), 
            instrumenttools.AltoVoice(),
            ])
