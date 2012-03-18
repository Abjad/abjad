from abjad import *


def test_instrumenttools_BassVoice__tools_package_qualified_indented_repr_01():

    voice = instrumenttools.BassVoice()

    assert voice._tools_package_qualified_indented_repr == "instrumenttools.BassVoice(\n\tinstrument_name='bass voice',\n\tinstrument_name_markup=markuptools.Markup(\n\t\t'Bass voice',\n\t\tstyle_string='backslash'\n\t\t),\n\tshort_instrument_name='bass',\n\tshort_instrument_name_markup=markuptools.Markup(\n\t\t'Bass',\n\t\tstyle_string='backslash'\n\t\t)\n\t)"
