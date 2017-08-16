import abjad
import pytest


def test_scoretools_Tuplet_from_leaf_and_ratio_01():

    note = abjad.Note(0, (3, 16))

    tuplet = abjad.Tuplet.from_leaf_and_ratio(note, [1], is_diminution=False)

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(note, [1, 2], is_diminution=False)

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        [1, 2, 2, 3],
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'64
            c'32
            c'32
            c'32.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        [1, 2, 2, 3, 3],
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 12/11 {
            c'64
            c'32
            c'32
            c'32.
            c'32.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        [1, 2, 2, 3, 3, 4],
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 8/5 {
            c'128
            c'64
            c'64
            c'64.
            c'64.
            c'32
        }
        '''
        )


def test_scoretools_Tuplet_from_leaf_and_ratio_02():

    note = abjad.Note("c'8.")

    tuplet = abjad.Tuplet.from_leaf_and_ratio(note, [1], is_diminution=True)

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(note, [1, 2], is_diminution=True)

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(note, [1, 2, 2, 3], is_diminution=True)

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'32
            c'16
            c'16
            c'16.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        [1, 2, 2, 3, 3],
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/11 {
            c'32
            c'16
            c'16
            c'16.
            c'16.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        [1, 2, 2, 3, 3, 4],
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 4/5 {
            c'64
            c'32
            c'32
            c'32.
            c'32.
            c'16
        }
        '''
        )


def test_scoretools_Tuplet_from_leaf_and_ratio_03():
    r'''Divide note into 1, ..., 5 parts.
    '''

    note = abjad.Note("c'8.")

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        1 * [1],
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        2 * [1],
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16.
            c'16.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        3 * [1],
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        4 * [1],
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'32.
            c'32.
            c'32.
            c'32.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        5 * [1],
        is_diminution=False,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 8/5 {
            c'64.
            c'64.
            c'64.
            c'64.
            c'64.
        }
        '''
        )


def test_scoretools_Tuplet_from_leaf_and_ratio_04():
    r'''Divide note into 1, ..., 5 parts.
    '''

    note = abjad.Note("c'8.")

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        1 * [1],
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        2 * [1],
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16.
            c'16.
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        3 * [1],
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = abjad.Tuplet.from_leaf_and_ratio(
        note,
        4 * [1],
        is_diminution=True,
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'32.
            c'32.
            c'32.
            c'32.
        }
        '''
        )
