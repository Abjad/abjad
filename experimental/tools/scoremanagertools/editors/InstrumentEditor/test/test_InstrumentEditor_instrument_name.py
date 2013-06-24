from abjad import *
from experimental import *


def test_InstrumentEditor_instrument_name_01():
    '''Quit, back & home all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers hornist horn in q')
    assert score_manager._session.transcript.signature == (13,)

    score_manager._run(pending_user_input='red~example~score setup performers hornist horn in b q')
    assert score_manager._session.transcript.signature == (15, (10, 13))

    score_manager._run(pending_user_input='red~example~score setup performers hornist horn in home q')
    assert score_manager._session.transcript.signature == (15, (0, 13))


def test_InstrumentEditor_instrument_name_02():
    '''String only.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='red~example~score setup performers hornist horn in -99 q')
    assert score_manager._session.transcript.signature == (15,)


def test_InstrumentEditor_instrument_name_03():
    '''Instrument name changes instrument name markup.
    Unless instrument name markup is set explicitly.
    '''

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input="accordion in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == markuptools.Markup('Foo')

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input="accordion im 'bar' in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == markuptools.Markup('bar')
