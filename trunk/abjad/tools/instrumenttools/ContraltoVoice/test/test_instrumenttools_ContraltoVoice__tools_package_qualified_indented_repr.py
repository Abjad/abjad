from abjad import *


def test_instrumenttools_ContraltoVoice__tools_package_qualified_indented_repr_01():

    voice = instrumenttools.ContraltoVoice()

    assert voice._tools_package_qualified_indented_repr == "instrumenttools.ContraltoVoice(\n\tinstrument_name='contralto voice',\n\tinstrument_name_markup=markuptools.Markup(\n\t\t'Contralto voice',\n\t\tstyle_string='backslash'\n\t\t),\n\tshort_instrument_name='contralto',\n\tshort_instrument_name_markup=markuptools.Markup(\n\t\t'Contralto',\n\t\tstyle_string='backslash'\n\t\t)\n\t)"

