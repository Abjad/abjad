from abjad import *
from experimental import *


def test_InstrumentEditor_short_instrument_name_01():
    '''Quit, back & studio all work.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i setup perf hornist horn sn q')
    assert studio.ts == (13,)

    studio.run(user_input='example~score~i setup performers hornist horn sn b q')
    assert studio.ts == (15, (10, 13))

    studio.run(user_input='example~score~i setup performers hornist horn sn studio q')
    assert studio.ts == (15, (0, 13))


def test_InstrumentEditor_short_instrument_name_02():
    '''String only.
    '''

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i setup performers hornist horn sn -99 q')
    assert studio.ts == (15,)


def test_InstrumentEditor_short_instrument_name_03():
    '''Short instrument name changes short instrument name markup.
    Unless short instrument name markup is set explicitly.
    '''

    editor = scoremanagementtools.editors.InstrumentEditor()
    editor.run(user_input="accordion sn 'foo' q")
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('Foo')

    editor = scoremanagementtools.editors.InstrumentEditor()
    editor.run(user_input="accordion sm 'bar' sn 'foo' q")
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('bar')
