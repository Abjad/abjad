from abjad import *


def test_instrumenttools_Flute__tools_package_qualified_indented_repr_01():

    flute = instrumenttools.Flute()

    assert flute._tools_package_qualified_indented_repr == "instrumenttools.Flute(\n\tinstrument_name='flute',\n\tinstrument_name_markup=markuptools.Markup(\n\t\t'Flute',\n\t\tstyle_string='backslash'\n\t\t),\n\tshort_instrument_name='fl.',\n\tshort_instrument_name_markup=markuptools.Markup(\n\t\t'Fl.',\n\t\tstyle_string='backslash'\n\t\t)\n\t)"
