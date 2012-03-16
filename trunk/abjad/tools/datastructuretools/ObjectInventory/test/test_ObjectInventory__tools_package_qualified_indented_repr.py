from abjad import *
from abjad.tools import datastructuretools


def test_ObjectInventory__tools_package_qualified_indented_repr_01():

    inventory = datastructuretools.ObjectInventory([
        'foo',
        instrumenttools.Flute(), 
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah'])

    assert repr(inventory) == "ObjectInventory(['foo', Flute(), 'bar', PitchRange('[A0, C8]'), 'blah'])"

    r'''
    datastructuretools.ObjectInventory([
        'foo',
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
        'bar',
        pitchtools.PitchRange(
            '[A0, C8]'
            ),
        'blah'
        ])
    '''

    assert inventory._tools_package_qualified_indented_repr == "datastructuretools.ObjectInventory([\n\t'foo',\n\tinstrumenttools.Flute(\n\t\tinstrument_name='flute',\n\t\tinstrument_name_markup=markuptools.Markup(\n\t\t\t'Flute',\n\t\t\tstyle_string='backslash'\n\t\t\t),\n\t\tshort_instrument_name='fl.',\n\t\tshort_instrument_name_markup=markuptools.Markup(\n\t\t\t'Fl.',\n\t\t\tstyle_string='backslash'\n\t\t\t)\n\t\t),\n\t'bar',\n\tpitchtools.PitchRange(\n\t\t'[A0, C8]'\n\t\t),\n\t'blah'\n\t])"


def test_ObjectInventory__tools_package_qualified_indented_repr_02():

    '''Empty inventory.
    '''

    inventory = datastructuretools.ObjectInventory()

    assert repr(inventory) == 'ObjectInventory([])'
    assert inventory._tools_package_qualified_repr == 'datastructuretools.ObjectInventory([])'
    assert inventory._tools_package_qualified_indented_repr == 'datastructuretools.ObjectInventory([])'
