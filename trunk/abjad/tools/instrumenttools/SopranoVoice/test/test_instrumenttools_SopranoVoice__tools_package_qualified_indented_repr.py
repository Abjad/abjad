from abjad import *


def test_instrumenttools_SopranoVoice__tools_package_qualified_indented_repr_01():

    voice = instrumenttools.SopranoVoice()

    assert voice._tools_package_qualified_indented_repr == "instrumenttools.SopranoVoice(\n\tinstrument_name='soprano voice',\n\tinstrument_name_markup=markuptools.Markup(\n\t\t'Soprano voice',\n\t\tstyle_string='backslash'\n\t\t),\n\tshort_instrument_name='soprano',\n\tshort_instrument_name_markup=markuptools.Markup(\n\t\t'Soprano',\n\t\tstyle_string='backslash'\n\t\t)\n\t)"
