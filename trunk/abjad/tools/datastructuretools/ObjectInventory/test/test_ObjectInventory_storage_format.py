from abjad import *
from abjad.tools import datastructuretools


def test_ObjectInventory_storage_format_01():
    '''Empty inventory. No keywords.
    '''

    inventory = datastructuretools.ObjectInventory()

    assert repr(inventory) == 'ObjectInventory([])'
    assert inventory.storage_format == 'datastructuretools.ObjectInventory([])'


def test_ObjectInventory_storage_format_02():
    '''Empty inventory. With keywords.
    '''

    inventory = datastructuretools.ObjectInventory(name='foo')

    assert repr(inventory) == "ObjectInventory([], name='foo')"
    assert inventory.storage_format == "datastructuretools.ObjectInventory([],\n\tname='foo'\n\t)"


def test_ObjectInventory_storage_format_03():
    '''Populated inventory. Without keywords.
    '''

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
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange(
            '[A0, C8]'
            ),
        'blah'
        ])
    '''

    assert inventory._storage_format == "datastructuretools.ObjectInventory([\n\t'foo',\n\tinstrumenttools.Flute(),\n\t'bar',\n\tpitchtools.PitchRange(\n\t\t'[A0, C8]'\n\t\t),\n\t'blah'\n\t])"


def test_ObjectInventory_storage_format_04():
    '''Populated inventory. With keywords.
    '''

    inventory = datastructuretools.ObjectInventory([
        'foo',
        instrumenttools.Flute(), 
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah'],
        name='foo')

    r'''
    datastructuretools.ObjectInventory([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange(
            '[A0, C8]'
            ),
        'blah'
        ],
        name='foo'
        )
    '''

    assert inventory._storage_format == "datastructuretools.ObjectInventory([\n\t'foo',\n\tinstrumenttools.Flute(),\n\t'bar',\n\tpitchtools.PitchRange(\n\t\t'[A0, C8]'\n\t\t),\n\t'blah'\n\t],\n\tname='foo'\n\t)"
