# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentEditor_short_instrument_name_01():
    r'''Quit, back & home all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn sn q')
    assert score_manager.session.io_transcript.signature == (13,)

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn sn b q')
    assert score_manager.session.io_transcript.signature == (15, (10, 13))

    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn sn home q')
    assert score_manager.session.io_transcript.signature == (15, (0, 13))


def test_InstrumentEditor_short_instrument_name_02():
    r'''String only.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score score~setup instrumentation hornist horn sn -99 q')
    assert score_manager.session.io_transcript.signature == (15,)


def test_InstrumentEditor_short_instrument_name_03():
    r'''Short instrument name does not change short instrument name markup.
    Unless short instrument name markup is set explicitly.
    '''

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input="accordion sn 'foo' q")
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input="accordion sm 'bar' sn 'foo' q")
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('bar')
