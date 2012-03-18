from abjad import *


def test_instrumenttools_MezzoSopranoVoice__tools_package_qualified_indented_repr_01():

    voice = instrumenttools.MezzoSopranoVoice()

    assert voice._tools_package_qualified_indented_repr == "instrumenttools.MezzoSopranoVoice(\n\tinstrument_name='mezzo-soprano voice',\n\tinstrument_name_markup=markuptools.Markup(\n\t\t'Mezzo-soprano voice',\n\t\tstyle_string='backslash'\n\t\t),\n\tshort_instrument_name='mezzo-soprano',\n\tshort_instrument_name_markup=markuptools.Markup(\n\t\t'Mezzo-soprano',\n\t\tstyle_string='backslash'\n\t\t)\n\t)"
