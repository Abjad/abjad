# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerEditor_name_01():
    r'''Quit, back and home all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist name q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (11,)

    input_ = 'red~example~score setup instrumentation hornist name b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13, (8, 11))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist name h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13, (0, 11))


def test_PerformerEditor_name_02():
    r'''input_ input only.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist name -99 q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13,)


def test_PerformerEditor_name_03():
    r'''Create, name and rename performer.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.PerformerEditor(session=session)
    input_ = 'name foo name bar q'
    editor._run(pending_user_input=input_)
    assert editor.target == instrumenttools.Performer(name='bar')
