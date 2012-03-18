from abjad import *


def test_instrumenttools_BaritoneVoice__tools_package_qualified_indented_repr_01():

    voice = instrumenttools.BaritoneVoice()

    assert voice._tools_package_qualified_indented_repr == "instrumenttools.BaritoneVoice(\n\tinstrument_name='baritone voice',\n\tinstrument_name_markup=markuptools.Markup(\n\t\t'Baritone voice',\n\t\tstyle_string='backslash'\n\t\t),\n\tshort_instrument_name='baritone',\n\tshort_instrument_name_markup=markuptools.Markup(\n\t\t'Baritone',\n\t\tstyle_string='backslash'\n\t\t)\n\t)"
