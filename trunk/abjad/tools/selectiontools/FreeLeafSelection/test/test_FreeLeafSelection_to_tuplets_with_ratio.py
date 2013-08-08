# -*- encoding: utf-8 -*-
from abjad import *
import py
py.test.skip('FIXME: bind functionality to correct selection class')


def test_FreeLeafSelection_to_tuplets_with_ratio_01():

    note = Note(0, (3, 16))
    selection = selectiontools.select_leaves(note)

    tuplets = selection.to_tuplets_with_ratio([1], is_diminution=False)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'8.
        }
        '''
        )

    tuplets = selection.to_tuplets_with_ratio([1, 2], is_diminution=False)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    # TODO: DECIDE ON DOTTED VALUES #
    #tuplets = selection.to_tuplets_with_ratio([1, 2, 2], is_diminution=False)
    #assert tuplets[0].lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 6/5 {\n\tc'32\n\tc'16\n\tc'16\n}"

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3], is_diminution=False)
    assert testtools.compare(
        tuplets[0].lilypond_format,
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

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3, 3], is_diminution=False)
    assert testtools.compare(
        tuplets[0].lilypond_format,
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

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3, 3, 4], is_diminution=False)
    assert testtools.compare(
        tuplets[0].lilypond_format,
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


def test_FreeLeafSelection_to_tuplets_with_ratio_02():

    note = Note("c'8.")
    selection = selectiontools.select_leaves(note)

    tuplets = selection.to_tuplets_with_ratio([1], is_diminution=True)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'8.
        }
        '''
        )

    tuplets = selection.to_tuplets_with_ratio([1, 2], is_diminution=True)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'16
            c'8
        }
        '''
        )

    # TODO: DECIDE ON DOTTED VALUES #
    #tuplets = selection.to_tuplets_with_ratio([1, 2, 2], is_diminution=True)
    #assert tuplets[0].lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/5 {\n\tc'16\n\tc'8\n\tc'8\n}"

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3], is_diminution=True)
    assert testtools.compare(
        tuplets[0].lilypond_format,
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

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3, 3], is_diminution=True)
    assert testtools.compare(
        tuplets[0].lilypond_format,
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

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3, 3, 4], is_diminution=True)
    assert testtools.compare(
        tuplets[0].lilypond_format,
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


def test_FreeLeafSelection_to_tuplets_with_ratio_03():
    r'''Divide note into 1, ..., 5 parts.
    '''

    note = Note("c'8.")
    selection = selectiontools.select_leaves(note)

    tuplets =selection.to_tuplets_with_ratio(1 * [1], is_diminution=False)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'8.
        }
        '''
        )

    tuplets =selection.to_tuplets_with_ratio(2 * [1], is_diminution=False)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'16.
            c'16.
        }
        '''
        )

    tuplets =selection.to_tuplets_with_ratio(3 * [1], is_diminution=False)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplets =selection.to_tuplets_with_ratio(4 * [1], is_diminution=False)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'32.
            c'32.
            c'32.
            c'32.
        }
        '''
        )

    tuplets =selection.to_tuplets_with_ratio(5 * [1], is_diminution=False)
    assert testtools.compare(
        tuplets[0].lilypond_format,
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


def test_FreeLeafSelection_to_tuplets_with_ratio_04():
    r'''Divide note into 1, ..., 5 parts.
    '''

    note = Note("c'8.")
    selection = selectiontools.select_leaves(note)

    tuplets =selection.to_tuplets_with_ratio(1 * [1], is_diminution=True)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'8.
        }
        '''
        )

    tuplets =selection.to_tuplets_with_ratio(2 * [1], is_diminution=True)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'16.
            c'16.
        }
        '''
        )

    tuplets =selection.to_tuplets_with_ratio(3 * [1], is_diminution=True)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'16
            c'16
            c'16
        }
        '''
        )

    tuplets =selection.to_tuplets_with_ratio(4 * [1], is_diminution=True)
    assert testtools.compare(
        tuplets[0].lilypond_format,
        r'''
        {
            c'32.
            c'32.
            c'32.
            c'32.
        }
        '''
        )
