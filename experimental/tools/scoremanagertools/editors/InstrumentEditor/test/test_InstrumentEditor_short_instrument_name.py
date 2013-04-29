from abjad import *
from experimental import *


def test_InstrumentEditor_short_instrument_name_01():
    '''Quit, back & home all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup perf hornist horn sn q')
    assert score_manager.transcript_signature == (13,)

    score_manager.run(user_input='example~score~i setup performers hornist horn sn b q')
    assert score_manager.transcript_signature == (15, (10, 13))

    score_manager.run(user_input='example~score~i setup performers hornist horn sn home q')
    assert score_manager.transcript_signature == (15, (0, 13))


def test_InstrumentEditor_short_instrument_name_02():
    '''String only.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i setup performers hornist horn sn -99 q')
    assert score_manager.transcript_signature == (15,)


def test_InstrumentEditor_short_instrument_name_03():
    '''Short instrument name changes short instrument name markup.
    Unless short instrument name markup is set explicitly.
    '''

    editor = scoremanagertools.editors.InstrumentEditor()
    editor.run(user_input="accordion sn 'foo' q")
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('Foo')

    editor = scoremanagertools.editors.InstrumentEditor()
    editor.run(user_input="accordion sm 'bar' sn 'foo' q")
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('bar')
