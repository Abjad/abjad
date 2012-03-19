from abjad import *


def test_instrumenttools_Flute__tools_package_qualified_indented_repr_01():

    flute = instrumenttools.Flute()

    assert flute._tools_package_qualified_indented_repr == 'instrumenttools.Flute()'


def test_instrumenttools_Flute__tools_package_qualified_indented_repr_02():
    '''Works with explicit instrument name markup.
    '''

    flute = instrumenttools.Flute(instrument_name_markup=markuptools.Markup('Foo'))

    assert flute._tools_package_qualified_indented_repr == "instrumenttools.Flute(\n\tinstrument_name_markup=markuptools.Markup(\n\t\t'Foo'\n\t\t)\n\t)"
