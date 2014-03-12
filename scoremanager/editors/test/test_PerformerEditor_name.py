# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerEditor_name_01():
    r'''Quit, back and home all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation hornist name q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (11,)

    string = 'red~example~score setup instrumentation hornist name b q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (13, (8, 11))

    string = 'red~example~score setup instrumentation'
    string += ' hornist name h q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (13, (0, 11))


def test_PerformerEditor_name_02():
    r'''String input only.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation hornist name -99 q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (13,)


def test_PerformerEditor_name_03():
    r'''Create, name and rename performer.
    '''

    session = scoremanager.core.Session()
    editor = scoremanager.editors.PerformerEditor(session=session)
    editor._run(pending_user_input='name foo name bar q')
    assert editor.target == instrumenttools.Performer(name='bar')
