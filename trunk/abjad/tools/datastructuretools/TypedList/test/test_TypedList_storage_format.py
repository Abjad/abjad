# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import datastructuretools


def test_TypedList_storage_format_01():
    r'''Empty inventory. No keywords.
    '''

    inventory = datastructuretools.TypedList()

    assert repr(inventory) == 'TypedList([])'
    assert inventory.storage_format == 'datastructuretools.TypedList([])'


def test_TypedList_storage_format_02():
    r'''Empty inventory. With keywords.
    '''

    inventory = datastructuretools.TypedList(name='foo')

    assert repr(inventory) == "TypedList([], name='foo')"
    assert inventory.storage_format == "datastructuretools.TypedList([],\n\tname='foo'\n\t)"


def test_TypedList_storage_format_03():
    r'''Populated inventory. Without keywords.
    '''

    inventory = datastructuretools.TypedList([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah'])

    assert repr(inventory) == "TypedList(['foo', Flute(), 'bar', PitchRange('[A0, C8]'), 'blah'])"

    r'''
    datastructuretools.TypedList([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange(
            '[A0, C8]'
            ),
        'blah'
        ])
    '''

    assert inventory._storage_format == "datastructuretools.TypedList([\n\t'foo',\n\tinstrumenttools.Flute(),\n\t'bar',\n\tpitchtools.PitchRange(\n\t\t'[A0, C8]'\n\t\t),\n\t'blah'\n\t])"


def test_TypedList_storage_format_04():
    r'''Populated inventory. With keywords.
    '''

    inventory = datastructuretools.TypedList([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah'],
        name='foo')

    r'''
    datastructuretools.TypedList([
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

    assert inventory._storage_format == "datastructuretools.TypedList([\n\t'foo',\n\tinstrumenttools.Flute(),\n\t'bar',\n\tpitchtools.PitchRange(\n\t\t'[A0, C8]'\n\t\t),\n\t'blah'\n\t],\n\tname='foo'\n\t)"
