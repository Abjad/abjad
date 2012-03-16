from abjad import *


def test_InstrumentationSpecifier__tools_package_qualified_indented_repr_01():

    flute = scoretools.Performer('Flute')
    flute.instruments.append(instrumenttools.Flute())
    flute.instruments.append(instrumenttools.AltoFlute())
    guitar = scoretools.Performer('Guitar')
    guitar.instruments.append(instrumenttools.Guitar())
    specifier = scoretools.InstrumentationSpecifier([flute, guitar])
    
    r'''
    scoretools.InstrumentationSpecifier(
        performers=scoretools.PerformerInventory([
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
                ),
            scoretools.Performer(
                name='Guitar',
                instruments=instrumenttools.InstrumentInventory([
                    instrumenttools.Guitar(
                        instrument_name='guitar',
                        instrument_name_markup=markuptools.Markup(
                            'Guitar',
                            style_string='backslash'
                            ),
                        short_instrument_name='gt.',
                        short_instrument_name_markup=markuptools.Markup(
                            'Gt.',
                            style_string='backslash'
                            )
                        )
                    ])
                )
            ])
        )
    '''

    assert specifier._tools_package_qualified_indented_repr == "scoretools.InstrumentationSpecifier(\n\tperformers=scoretools.PerformerInventory([\n\t\tscoretools.Performer(\n\t\t\tname='Flute',\n\t\t\tinstruments=instrumenttools.InstrumentInventory([\n\t\t\t\tinstrumenttools.Flute(\n\t\t\t\t\tinstrument_name='flute',\n\t\t\t\t\tinstrument_name_markup=markuptools.Markup(\n\t\t\t\t\t\t'Flute',\n\t\t\t\t\t\tstyle_string='backslash'\n\t\t\t\t\t\t),\n\t\t\t\t\tshort_instrument_name='fl.',\n\t\t\t\t\tshort_instrument_name_markup=markuptools.Markup(\n\t\t\t\t\t\t'Fl.',\n\t\t\t\t\t\tstyle_string='backslash'\n\t\t\t\t\t\t)\n\t\t\t\t\t),\n\t\t\t\tinstrumenttools.AltoFlute(\n\t\t\t\t\tinstrument_name='alto flute',\n\t\t\t\t\tinstrument_name_markup=markuptools.Markup(\n\t\t\t\t\t\t'Alto flute',\n\t\t\t\t\t\tstyle_string='backslash'\n\t\t\t\t\t\t),\n\t\t\t\t\tshort_instrument_name='alt. fl.',\n\t\t\t\t\tshort_instrument_name_markup=markuptools.Markup(\n\t\t\t\t\t\t'Alt. fl.',\n\t\t\t\t\t\tstyle_string='backslash'\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t])\n\t\t\t),\n\t\tscoretools.Performer(\n\t\t\tname='Guitar',\n\t\t\tinstruments=instrumenttools.InstrumentInventory([\n\t\t\t\tinstrumenttools.Guitar(\n\t\t\t\t\tinstrument_name='guitar',\n\t\t\t\t\tinstrument_name_markup=markuptools.Markup(\n\t\t\t\t\t\t'Guitar',\n\t\t\t\t\t\tstyle_string='backslash'\n\t\t\t\t\t\t),\n\t\t\t\t\tshort_instrument_name='gt.',\n\t\t\t\t\tshort_instrument_name_markup=markuptools.Markup(\n\t\t\t\t\t\t'Gt.',\n\t\t\t\t\t\tstyle_string='backslash'\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t])\n\t\t\t)\n\t\t])\n\t)"
