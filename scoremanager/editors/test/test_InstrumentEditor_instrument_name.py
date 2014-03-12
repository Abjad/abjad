# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_instrument_name_01():
    r'''Quit, back & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation hornist horn in q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (13,)

    string = 'red~example~score setup instrumentation'
    string += ' hornist horn in b q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (15, (10, 13))

    string = 'red~example~score setup instrumentation'
    string += ' hornist horn in h q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (15, (0, 13))


def test_InstrumentEditor_instrument_name_02():
    r'''String only.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation'
    string += ' hornist horn in -99 q'
    score_manager._run(pending_user_input=string, is_test=True)
    assert score_manager._transcript.signature == (15,)


def test_InstrumentEditor_instrument_name_03():
    r'''Instrument name does not change instrument name markup.
    '''

    session = scoremanager.core.Session()
    editor = scoremanager.editors.InstrumentEditor(session=session)
    editor._run(pending_user_input="accordion in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'

    session = scoremanager.core.Session()
    editor = scoremanager.editors.InstrumentEditor(session=session)
    editor._run(pending_user_input="accordion im 'bar' in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == markuptools.Markup('bar')
