# -*- coding: utf-8 -*-
import abjad


def test_selectiontools_Selection__all_in_same_parent_01():
    r'''Is true for strictly contiguous leaves in voice.
    Is false for other time orderings of leaves in voice.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    assert abjad.Selection._all_in_same_parent(voice[:])

    assert not abjad.Selection._all_in_same_parent(
        list(reversed(voice[:])))

    components = []
    components.extend(voice[2:])
    components.extend(voice[:2])
    assert not abjad.Selection._all_in_same_parent(
        components)

    components = []
    components.extend(voice[3:4])
    components.extend(voice[:1])
    assert not abjad.Selection._all_in_same_parent(
        components)
    components = [voice]
    components.extend(voice[:])
    assert not abjad.Selection._all_in_same_parent(
        components)


def test_selectiontools_Selection__all_in_same_parent_02():
    r'''Is true for unincorporated components when orphans allowed.
    Is false for unincorporated components when orphans not allowed.
    '''

    voice = abjad.Voice(r'''
        {
            c'8
            d'8
        }
        {
            e'8
            f'8
        }
        ''')

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.Selection._all_in_same_parent([voice])
    assert not abjad.Selection._all_in_same_parent(
        [voice], allow_orphans = False)

    assert abjad.Selection._all_in_same_parent(voice[:])

    assert abjad.Selection._all_in_same_parent(voice[0][:])
    assert abjad.Selection._all_in_same_parent(voice[1][:])

    leaves = abjad.select(voice).by_leaf()
    assert not abjad.Selection._all_in_same_parent(leaves)


def test_selectiontools_Selection__all_in_same_parent_03():
    r'''Is true for orphan leaves when allow_orphans is true.
    Is false for orphan leaves when allow_orphans is false.
    '''

    notes = [abjad.Note("c'8"), abjad.Note("d'8"), abjad.Note("e'8"), abjad.Note("f'8")]

    assert abjad.Selection._all_in_same_parent(notes)
    assert not abjad.Selection._all_in_same_parent(
        notes, allow_orphans=False)


def test_selectiontools_Selection__all_in_same_parent_04():
    r'''Empty list returns true.
    '''

    sequence = []

    assert abjad.Selection._all_in_same_parent(sequence)
