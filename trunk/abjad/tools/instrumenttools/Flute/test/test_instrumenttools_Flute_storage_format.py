from abjad import *


def test_instrumenttools_Flute_storage_format_01():

    flute = instrumenttools.Flute()

    assert flute.storage_format == 'instrumenttools.Flute()'


def test_instrumenttools_Flute_storage_format_02():
    '''Works with explicit instrument name markup.
    '''

    flute = instrumenttools.Flute(instrument_name_markup=markuptools.Markup('Foo'))

    assert flute.storage_format == "instrumenttools.Flute(\n\tinstrument_name_markup=markuptools.Markup((\n\t\t'Foo',\n\t\t))\n\t)"
