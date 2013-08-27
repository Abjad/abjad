# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_Tuplet_from_leaf_and_ratio_01():

    note = Note(0, (3, 16))

    tuplet = Tuplet.from_leaf_and_ratio(note, [1], is_diminution=False)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, [1, 2], is_diminution=False)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    # TODO: DECIDE ON DOTTED VALUES #
    #tuplet = Tuplet.from_leaf_and_ratio(note, [1, 2, 2], is_diminution=False)
    #assert tuplet.lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 6/5 {\n\tc'32\n\tc'16\n\tc'16\n}"

    tuplet = Tuplet.from_leaf_and_ratio(
        note, [1, 2, 2, 3], is_diminution=False)

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/2 {
            c'64
            c'32
            c'32
            c'32.
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, [1, 2, 2, 3, 3], is_diminution=False)

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 12/11 {
            c'64
            c'32
            c'32
            c'32.
            c'32.
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, [1, 2, 2, 3, 3, 4], is_diminution=False)

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
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


def test_Tuplet_from_leaf_and_ratio_02():

    note = Note("c'8.")

    tuplet = Tuplet.from_leaf_and_ratio(
        note, [1], is_diminution=True)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, [1, 2], is_diminution=True)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    # TODO: DECIDE ON DOTTED VALUES #
    #tuplet = Tuplet.from_leaf_and_ratio(note, [1, 2, 2], is_diminution=True)
    #assert tuplet.lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/5 {\n\tc'16\n\tc'8\n\tc'8\n}"

    tuplet = Tuplet.from_leaf_and_ratio(
        note, [1, 2, 2, 3], is_diminution=True)

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'32
            c'16
            c'16
            c'16.
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, [1, 2, 2, 3, 3], is_diminution=True)

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 6/11 {
            c'32
            c'16
            c'16
            c'16.
            c'16.
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, [1, 2, 2, 3, 3, 4], is_diminution=True)

    assert testtools.compare(
        tuplet,
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


def test_Tuplet_from_leaf_and_ratio_03():
    r'''Divide note into 1, ..., 5 parts.
    '''

    note = Note("c'8.")

    tuplet = Tuplet.from_leaf_and_ratio(
        note, 1 * [1], is_diminution=False)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, 2 * [1], is_diminution=False)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'16.
            c'16.
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, 3 * [1], is_diminution=False)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, 4 * [1], is_diminution=False)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'32.
            c'32.
            c'32.
            c'32.
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, 5 * [1], is_diminution=False)

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 8/5 {
            c'64.
            c'64.
            c'64.
            c'64.
            c'64.
        }
        '''
        )


def test_Tuplet_from_leaf_and_ratio_04():
    r'''Divide note into 1, ..., 5 parts.
    '''

    note = Note("c'8.")

    tuplet = Tuplet.from_leaf_and_ratio(
        note, 1 * [1], is_diminution=True)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'8.
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, 2 * [1], is_diminution=True)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'16.
            c'16.
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, 3 * [1], is_diminution=True)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplet = Tuplet.from_leaf_and_ratio(
        note, 4 * [1], is_diminution=True)

    assert testtools.compare(
        tuplet,
        r'''
        {
            c'32.
            c'32.
            c'32.
            c'32.
        }
        '''
        )
