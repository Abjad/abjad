# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerEditor_delete_instruments_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist rm q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (11,)

    input_ = 'red~example~score setup instrumentation hornist rm b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13, (8, 11))

    input_ = 'red~example~score setup instrumentation hornist rm h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13, (0, 11))

    input_ = 'red~example~score setup instrumentation hornist rm s q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13, (2, 11))

    input_ = 'red~example~score setup instrumentation hornist rm foo q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13, (8, 11))


def test_PerformerEditor_delete_instruments_02():
    r'''Add two instruments. Delete one.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.PerformerEditor(session=session)
    input_ = 'add flute add acc rm flute q'
    editor._run(pending_user_input=input_)
    assert editor.target == instrumenttools.Performer(
        instruments=[instrumenttools.Accordion()]
        )


def test_PerformerEditor_delete_instruments_03():
    r'''Numeric range handling.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.PerformerEditor(session=session)
    input_ = 'add 1-3 rm 1,3 q'
    editor._run(pending_user_input=input_)
    assert editor.target == instrumenttools.Performer(
        instruments=[instrumenttools.AltoVoice()],
        )
