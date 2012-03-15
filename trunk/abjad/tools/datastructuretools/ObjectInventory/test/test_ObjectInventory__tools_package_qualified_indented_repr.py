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

    assert inventory._tools_package_qualified_repr == "datastructuretools.ObjectInventory(['foo', instrumenttools.Flute(), 'bar', pitchtools.PitchRange('[A0, C8]'), 'blah'])"


    r'''
    datastructuretools.ObjectInventory([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange(
            '[A0, C8]'
            ),
        'blah'
        ])
    '''

    assert inventory._tools_package_qualified_indented_repr == "datastructuretools.ObjectInventory([\n\t'foo',\n\tinstrumenttools.Flute(),\n\t'bar',\n\tpitchtools.PitchRange(\n\t\t'[A0, C8]'\n\t\t),\n\t'blah'\n\t])"


def test_ObjectInventory__tools_package_qualified_indented_repr_02():
    '''Empty inventory.
    '''

    inventory = datastructuretools.ObjectInventory()

    assert repr(inventory) == 'ObjectInventory([])'
    assert inventory._tools_package_qualified_repr == 'datastructuretools.ObjectInventory([])'
    assert inventory._tools_package_qualified_indented_repr == 'datastructuretools.ObjectInventory([])'
