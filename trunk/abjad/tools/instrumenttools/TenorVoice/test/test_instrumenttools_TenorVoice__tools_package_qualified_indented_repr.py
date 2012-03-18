from abjad import *


def test_instrumenttools_TenorVoice__tools_package_qualified_indented_repr_01():

    voice = instrumenttools.TenorVoice()

    assert voice._tools_package_qualified_indented_repr == "instrumenttools.TenorVoice(\n\tinstrument_name='tenor voice',\n\tinstrument_name_markup=markuptools.Markup(\n\t\t'Tenor voice',\n\t\tstyle_string='backslash'\n\t\t),\n\tshort_instrument_name='tenor',\n\tshort_instrument_name_markup=markuptools.Markup(\n\t\t'Tenor',\n\t\tstyle_string='backslash'\n\t\t)\n\t)"
