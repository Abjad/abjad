# -*- encoding: utf-8 -*-
from abjad import *


def test_datastructuretools_TypedList___format___01():
    r'''Empty inventory. No keywords.
    '''

    inventory = datastructuretools.TypedList()

    assert systemtools.TestManager.compare(
        repr(inventory),
        'TypedList([])',
        )
    assert systemtools.TestManager.compare(
        format(inventory),
        'datastructuretools.TypedList([])',
        )


def test_datastructuretools_TypedList___format___02():
    r'''Empty inventory. With keywords.
    '''

    inventory = datastructuretools.TypedList(name='foo')

    assert systemtools.TestManager.compare(
        repr(inventory),
        r'''
        TypedList([], name='foo')
        ''',
        )

    assert systemtools.TestManager.compare(
        format(inventory),
        r'''
        datastructuretools.TypedList([],
            name='foo',
            )
        ''',
        )


def test_datastructuretools_TypedList___format___03():
    r'''Populated inventory. Without keywords.
    '''

    inventory = datastructuretools.TypedList([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah'])

    assert systemtools.TestManager.compare(
        repr(inventory),
        "TypedList(['foo', Flute(), 'bar', PitchRange('[A0, C8]'), 'blah'])",
        )

    assert systemtools.TestManager.compare(
        format(inventory),
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


def test_datastructuretools_TypedList___format___04():
    r'''Populated inventory. With keywords.
    '''

    inventory = datastructuretools.TypedList([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah'],
        name='foo')

    assert systemtools.TestManager.compare(
        format(inventory),
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
