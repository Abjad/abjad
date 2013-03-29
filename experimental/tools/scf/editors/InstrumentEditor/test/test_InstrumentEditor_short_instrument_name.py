from abjad import *
import scf


def test_InstrumentEditor_short_instrument_name_01():
    '''Quit, back & studio all work.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='1 setup perf 1 1 sn q')
    assert studio.ts == (13, (1, 7, 9))

    studio.run(user_input='1 setup performers 1 1 sn b q')
    assert studio.ts == (15, (1, 7, 9), (10, 13))

    studio.run(user_input='1 setup performers 1 1 sn studio q')
    assert studio.ts == (15, (0, 13), (1, 7, 9))


def test_InstrumentEditor_short_instrument_name_02():
    '''String only.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='1 setup performers 1 1 sn -99 q')
    assert studio.ts == (15, (1, 7, 9))


def test_InstrumentEditor_short_instrument_name_03():
    '''Short instrument name changes short instrument name markup.
    Unless short instrument name markup is set explicitly.
    '''

    editor = scf.editors.InstrumentEditor()
    editor.run(user_input="1 sn 'foo' q")
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('Foo')

    editor = scf.editors.InstrumentEditor()
    editor.run(user_input="1 sm 'bar' sn 'foo' q")
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('bar')
