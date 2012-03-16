from abjad import *


def test_Performer__tools_package_qualified_indented_repr_01():

    performer = scoretools.Performer('Flute')
    performer.instruments.append(instrumenttools.Flute())
    performer.instruments.append(instrumenttools.AltoFlute())

    r'''
    scoretools.Performer(
        name='Flute',
        instruments=instrumenttools.InstrumentInventory([
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
            instrumenttools.AltoFlute(
                instrument_name='alto flute',
                instrument_name_markup=markuptools.Markup(
                    'Alto flute',
                    style_string='backslash'
                    ),
                short_instrument_name='alt. fl.',
                short_instrument_name_markup=markuptools.Markup(
                    'Alt. fl.',
                    style_string='backslash'
                    )
                )
            ])
        )
    '''

    assert performer._tools_package_qualified_indented_repr == "scoretools.Performer(\n\tname='Flute',\n\tinstruments=instrumenttools.InstrumentInventory([\n\t\tinstrumenttools.Flute(\n\t\t\tinstrument_name='flute',\n\t\t\tinstrument_name_markup=markuptools.Markup(\n\t\t\t\t'Flute',\n\t\t\t\tstyle_string='backslash'\n\t\t\t\t),\n\t\t\tshort_instrument_name='fl.',\n\t\t\tshort_instrument_name_markup=markuptools.Markup(\n\t\t\t\t'Fl.',\n\t\t\t\tstyle_string='backslash'\n\t\t\t\t)\n\t\t\t),\n\t\tinstrumenttools.AltoFlute(\n\t\t\tinstrument_name='alto flute',\n\t\t\tinstrument_name_markup=markuptools.Markup(\n\t\t\t\t'Alto flute',\n\t\t\t\tstyle_string='backslash'\n\t\t\t\t),\n\t\t\tshort_instrument_name='alt. fl.',\n\t\t\tshort_instrument_name_markup=markuptools.Markup(\n\t\t\t\t'Alt. fl.',\n\t\t\t\tstyle_string='backslash'\n\t\t\t\t)\n\t\t\t)\n\t\t])\n\t)"

