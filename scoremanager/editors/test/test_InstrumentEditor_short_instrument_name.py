# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_short_instrument_name_01():
    r'''Quit, back & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation hornist horn sn q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (13,)

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn sn b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (10, 13))

    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn sn h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (0, 13))


def test_InstrumentEditor_short_instrument_name_02():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score setup instrumentation'
    input_ += ' hornist horn sn -99 q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15,)


def test_InstrumentEditor_short_instrument_name_03():
    r'''Short instrument name does not change short instrument name markup.
    Unless short instrument name markup is set explicitly.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = "accordion sn 'foo' q"
    editor._run(pending_user_input=input_)
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = "accordion sm 'bar' sn 'foo' q"
    editor._run(pending_user_input=input_)
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('bar')
