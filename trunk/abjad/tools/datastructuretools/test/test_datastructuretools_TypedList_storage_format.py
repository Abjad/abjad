# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import datastructuretools


def test_datastructuretools_TypedList_storage_format_01():
    r'''Empty inventory. No keywords.
    '''

    inventory = datastructuretools.TypedList()

    assert testtools.compare(
        repr(inventory),
        'TypedList([])',
        )
    assert testtools.compare(
        inventory.storage_format,
        'datastructuretools.TypedList([])',
        )


def test_datastructuretools_TypedList_storage_format_02():
    r'''Empty inventory. With keywords.
    '''

    inventory = datastructuretools.TypedList(name='foo')

    assert testtools.compare(
        repr(inventory),
        r'''
        TypedList([], name='foo')
        ''',
        )

    assert testtools.compare(
        inventory.storage_format,
        r'''
        datastructuretools.TypedList([],
            name='foo',
            )
        ''',
        )


def test_datastructuretools_TypedList_storage_format_03():
    r'''Populated inventory. Without keywords.
    '''

    inventory = datastructuretools.TypedList([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah'])

    assert testtools.compare(
        repr(inventory),
        "TypedList(['foo', Flute(), 'bar', PitchRange('[A0, C8]'), 'blah'])",
        )

    assert testtools.compare(
        inventory.storage_format,
        r'''
        datastructuretools.TypedList([
            'foo',
            instrumenttools.Flute(),
            'bar',
            pitchtools.PitchRange(
                '[A0, C8]'
                ),
            'blah',
            ])
        ''',
        )


def test_datastructuretools_TypedList_storage_format_04():
    r'''Populated inventory. With keywords.
    '''

    inventory = datastructuretools.TypedList([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah'],
        name='foo')

    assert testtools.compare(
        inventory.storage_format,
        r'''
        datastructuretools.TypedList([
            'foo',
            instrumenttools.Flute(),
            'bar',
            pitchtools.PitchRange(
                '[A0, C8]'
                ),
            'blah',
            ],
            name='foo',
            )
        ''',
        )
