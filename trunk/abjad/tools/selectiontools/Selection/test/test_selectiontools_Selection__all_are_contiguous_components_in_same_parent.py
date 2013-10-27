# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.selectiontools import Selection


def test_selectiontools_Selection__all_are_contiguous_components_in_same_parent_01():
    r'''True for strictly contiguous leaves in voice.
    False for other time orderings of leaves in voice.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")

    assert Selection._all_are_contiguous_components_in_same_parent(
        voice.select_leaves())

    assert not Selection._all_are_contiguous_components_in_same_parent(
        list(reversed(voice.select_leaves())))

    components = []
    components.extend(voice.select_leaves()[2:])
    components.extend(voice.select_leaves()[:2])
    assert not Selection._all_are_contiguous_components_in_same_parent(
        components)

    components = []
    components.extend(voice.select_leaves()[3:4])
    components.extend(voice.select_leaves()[0:1])
    assert not Selection._all_are_contiguous_components_in_same_parent(
        components)
    components = [voice]
    components.extend(voice.select_leaves())
    assert not Selection._all_are_contiguous_components_in_same_parent(
        components)


def test_selectiontools_Selection__all_are_contiguous_components_in_same_parent_02():
    r'''True for unincorporated components when orphans allowed.
    False to unincorporated components when orphans not allowed.
    '''

    voice = Voice(r'''
        {
            c'8
            d'8
        }
        {
            e'8
            f'8
        }
        ''')

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
        '''
        )

    assert Selection._all_are_contiguous_components_in_same_parent([voice])
    assert not Selection._all_are_contiguous_components_in_same_parent(
        [voice], allow_orphans = False)

    assert Selection._all_are_contiguous_components_in_same_parent(voice[:])

    assert Selection._all_are_contiguous_components_in_same_parent(voice[0][:])
    assert Selection._all_are_contiguous_components_in_same_parent(voice[1][:])

    assert not Selection._all_are_contiguous_components_in_same_parent(
        voice.select_leaves())


def test_selectiontools_Selection__all_are_contiguous_components_in_same_parent_03():
    r'''True for orphan leaves when allow_orphans is True.
    False for orphan leaves when allow_orphans is False.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    assert Selection._all_are_contiguous_components_in_same_parent(notes)
    assert not Selection._all_are_contiguous_components_in_same_parent(
        notes, allow_orphans=False)


def test_selectiontools_Selection__all_are_contiguous_components_in_same_parent_04():
    r'''Empty list returns True.
    '''

    sequence = []

    assert Selection._all_are_contiguous_components_in_same_parent(sequence)
