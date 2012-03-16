from abjad import *


def test_InstrumentInventory__tools_package_qualified_indented_repr_01():

    inventory = instrumenttools.InstrumentInventory([
        instrumenttools.Flute(),
        instrumenttools.Violin()])

    r'''
    instrumenttools.InstrumentInventory([
        instrumenttools.Flute(
            instrument_name='flute',
            instrument_name_markup=markuptools.Markup(
                'Flute',
                style_string='backslash'
                ),
            short_instrument_name='fl.',
            short_instrument_name_markup=markuptools.Markup(
                'Fl.',
                style_string='backslash'
                )
            ),
        instrumenttools.Violin(
            instrument_name='violin',
            instrument_name_markup=markuptools.Markup(
                'Violin',
                style_string='backslash'
                ),
            short_instrument_name='vn.',
            short_instrument_name_markup=markuptools.Markup(
                'Vn.',
                style_string='backslash'
                )
            )
        ])
    '''

    assert inventory._tools_package_qualified_indented_repr == "instrumenttools.InstrumentInventory([\n\tinstrumenttools.Flute(\n\t\tinstrument_name='flute',\n\t\tinstrument_name_markup=markuptools.Markup(\n\t\t\t'Flute',\n\t\t\tstyle_string='backslash'\n\t\t\t),\n\t\tshort_instrument_name='fl.',\n\t\tshort_instrument_name_markup=markuptools.Markup(\n\t\t\t'Fl.',\n\t\t\tstyle_string='backslash'\n\t\t\t)\n\t\t),\n\tinstrumenttools.Violin(\n\t\tinstrument_name='violin',\n\t\tinstrument_name_markup=markuptools.Markup(\n\t\t\t'Violin',\n\t\t\tstyle_string='backslash'\n\t\t\t),\n\t\tshort_instrument_name='vn.',\n\t\tshort_instrument_name_markup=markuptools.Markup(\n\t\t\t'Vn.',\n\t\t\tstyle_string='backslash'\n\t\t\t)\n\t\t)\n\t])"
