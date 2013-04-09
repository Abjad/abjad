from abjad import *
import scftools


def test_InstrumentEditor_instrument_name_01():
    '''Quit, back & studio all work.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='1 setup performers 1 1 in q')
    assert studio.ts == (13, (1, 7, 9))

    studio.run(user_input='1 setup performers 1 1 in b q')
    assert studio.ts == (15, (1, 7, 9), (10, 13))

    studio.run(user_input='1 setup performers 1 1 in studio q')
    assert studio.ts == (15, (0, 13), (1, 7, 9))


def test_InstrumentEditor_instrument_name_02():
    '''String only.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='1 setup performers 1 1 in -99 q')
    assert studio.ts == (15, (1, 7, 9))


def test_InstrumentEditor_instrument_name_03():
    '''Instrument name changes instrument name markup.
    Unless instrument name markup is set explicitly.
    '''

    editor = scftools.editors.InstrumentEditor()
    editor.run(user_input="1 in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == markuptools.Markup('Foo')

    editor = scftools.editors.InstrumentEditor()
    editor.run(user_input="1 im 'bar' in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == markuptools.Markup('bar')
