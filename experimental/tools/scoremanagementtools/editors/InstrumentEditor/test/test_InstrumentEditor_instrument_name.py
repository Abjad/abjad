from abjad import *
from experimental import *


def test_InstrumentEditor_instrument_name_01():
    '''Quit, back & studio all work.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example setup performers hornist horn in q')
    assert studio.ts == (13,)

    studio.run(user_input='example setup performers hornist horn in b q')
    assert studio.ts == (15, (10, 13))

    studio.run(user_input='example setup performers hornist horn in studio q')
    assert studio.ts == (15, (0, 13))


def test_InstrumentEditor_instrument_name_02():
    '''String only.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example setup performers hornist horn in -99 q')
    assert studio.ts == (15,)


def test_InstrumentEditor_instrument_name_03():
    '''Instrument name changes instrument name markup.
    Unless instrument name markup is set explicitly.
    '''

    editor = scoremanagementtools.editors.InstrumentEditor()
    editor.run(user_input="accordion in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == markuptools.Markup('Foo')

    editor = scoremanagementtools.editors.InstrumentEditor()
    editor.run(user_input="accordion im 'bar' in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == markuptools.Markup('bar')
