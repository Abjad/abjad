# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_instrument_name_01():
    r'''Quit, back & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist horn in q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13,)

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn in b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (10, 13))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn in h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (0, 13))


def test_InstrumentEditor_instrument_name_02():
    r'''input_ only.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn in -99 q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15,)


def test_InstrumentEditor_instrument_name_03():
    r'''Instrument name does not change instrument name markup.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    editor._run(pending_user_input="accordion in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = "accordion im 'bar' in 'foo' q"
    editor._run(pending_user_input=input_)
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == markuptools.Markup('bar')
