from abjad import *


def test_instrumenttools_UntunedPercussion___repr___01():
    '''Without instrument name.
    '''

    instrument = instrumenttools.UntunedPercussion()

    r'''
    instrumenttools.UntunedPercussion(
        instrument_name='untuned percussion',
        instrument_name_markup=markuptools.Markup(
            'Untuned percussion',
            style_string='backslash'
            ),
        short_instrument_name='perc.',
        short_instrument_name_markup=markuptools.Markup(
            'Perc.',
            style_string='backslash'
            )
        )
    '''

    assert instrument._tools_package_qualified_indented_repr == "instrumenttools.UntunedPercussion(\n\tinstrument_name='untuned percussion',\n\tinstrument_name_markup=markuptools.Markup(\n\t\t'Untuned percussion',\n\t\tstyle_string='backslash'\n\t\t),\n\tshort_instrument_name='perc.',\n\tshort_instrument_name_markup=markuptools.Markup(\n\t\t'Perc.',\n\t\tstyle_string='backslash'\n\t\t)\n\t)"

    
def test_instrumenttools_UntunedPercussion___repr___02():
    '''With instrument name.
    '''

    instrument = instrumenttools.UntunedPercussion()
    instrument.instrument_name = 'rattle'
    instrument.short_instrument_name = 'rt.'

    r'''
    instrumenttools.UntunedPercussion(
        instrument_name='rattle',
        instrument_name_markup=markuptools.Markup(
            'Rattle',
            style_string='backslash'
            ),
        short_instrument_name='rt.',
        short_instrument_name_markup=markuptools.Markup(
            'Rt.',
            style_string='backslash'
            )
        )
    '''

    assert instrument._tools_package_qualified_indented_repr == "instrumenttools.UntunedPercussion(\n\tinstrument_name='rattle',\n\tinstrument_name_markup=markuptools.Markup(\n\t\t'Rattle',\n\t\tstyle_string='backslash'\n\t\t),\n\tshort_instrument_name='rt.',\n\tshort_instrument_name_markup=markuptools.Markup(\n\t\t'Rt.',\n\t\tstyle_string='backslash'\n\t\t)\n\t)"
