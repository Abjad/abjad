# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentEditor_instrument_name_01():
    r'''Quit, back & home all work.
    '''

    score_manager = scoremanagertools.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn in q')
    assert score_manager.session.io_transcript.signature == (13,)

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn in b q')
    assert score_manager.session.io_transcript.signature == (15, (10, 13))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn in home q')
    assert score_manager.session.io_transcript.signature == (15, (0, 13))


def test_InstrumentEditor_instrument_name_02():
    r'''String only.
    '''

    score_manager = scoremanagertools.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn in -99 q')
    assert score_manager.session.io_transcript.signature == (15,)


def test_InstrumentEditor_instrument_name_03():
    r'''Instrument name does not change instrument name markup.
    '''

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input="accordion in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input="accordion im 'bar' in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == markuptools.Markup('bar')
