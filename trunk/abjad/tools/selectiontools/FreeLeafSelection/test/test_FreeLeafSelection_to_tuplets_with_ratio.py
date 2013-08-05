# -*- encoding: utf-8 -*-
from abjad import *


def test_FreeLeafSelection_to_tuplets_with_ratio_01():

    note = Note(0, (3, 16))
    selection = selectiontools.select_leaves(note)

    tuplets = selection.to_tuplets_with_ratio([1], is_diminution=False)
    assert tuplets[0].lilypond_format == "{\n\tc'8.\n}"

    tuplets = selection.to_tuplets_with_ratio([1, 2], is_diminution=False)
    assert tuplets[0].lilypond_format == "{\n\tc'16\n\tc'8\n}"

    # TODO: DECIDE ON DOTTED VALUES #
    #tuplets = selection.to_tuplets_with_ratio([1, 2, 2], is_diminution=False)
    #assert tuplets[0].lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 6/5 {\n\tc'32\n\tc'16\n\tc'16\n}"

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3], is_diminution=False)
    assert tuplets[0].lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/2 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n}"

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3, 3], is_diminution=False)
    assert tuplets[0].lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 12/11 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n}"

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3, 3, 4], is_diminution=False)
    assert tuplets[0].lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 8/5 {\n\tc'128\n\tc'64\n\tc'64\n\tc'64.\n\tc'64.\n\tc'32\n}"


def test_FreeLeafSelection_to_tuplets_with_ratio_02():

    note = Note("c'8.")
    selection = selectiontools.select_leaves(note)

    tuplets = selection.to_tuplets_with_ratio([1], is_diminution=True)
    assert tuplets[0].lilypond_format == "{\n\tc'8.\n}"

    tuplets = selection.to_tuplets_with_ratio([1, 2], is_diminution=True)
    assert tuplets[0].lilypond_format == "{\n\tc'16\n\tc'8\n}"

    # TODO: DECIDE ON DOTTED VALUES #
    #tuplets = selection.to_tuplets_with_ratio([1, 2, 2], is_diminution=True)
    #assert tuplets[0].lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/5 {\n\tc'16\n\tc'8\n\tc'8\n}"

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3], is_diminution=True)
    assert tuplets[0].lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 3/4 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n}"

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3, 3], is_diminution=True)
    assert tuplets[0].lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 6/11 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n\tc'16.\n}"

    tuplets = selection.to_tuplets_with_ratio([1, 2, 2, 3, 3, 4], is_diminution=True)
    assert tuplets[0].lilypond_format == "\\times 4/5 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n\tc'16\n}"


def test_FreeLeafSelection_to_tuplets_with_ratio_03():
    r'''Divide note into 1, ..., 5 parts.
    '''

    note = Note("c'8.")
    selection = selectiontools.select_leaves(note)

    tuplets =selection.to_tuplets_with_ratio(1 * [1], is_diminution=False)
    assert tuplets[0].lilypond_format == "{\n\tc'8.\n}"

    tuplets =selection.to_tuplets_with_ratio(2 * [1], is_diminution=False)
    assert tuplets[0].lilypond_format == "{\n\tc'16.\n\tc'16.\n}"

    tuplets =selection.to_tuplets_with_ratio(3 * [1], is_diminution=False)
    assert tuplets[0].lilypond_format == "{\n\tc'16\n\tc'16\n\tc'16\n}"

    tuplets =selection.to_tuplets_with_ratio(4 * [1], is_diminution=False)
    assert tuplets[0].lilypond_format == "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"

    tuplets =selection.to_tuplets_with_ratio(5 * [1], is_diminution=False)
    assert tuplets[0].lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 8/5 {\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n}"


def test_FreeLeafSelection_to_tuplets_with_ratio_04():
    r'''Divide note into 1, ..., 5 parts.
    '''

    note = Note("c'8.")
    selection = selectiontools.select_leaves(note)

    tuplets =selection.to_tuplets_with_ratio(1 * [1], is_diminution=True)
    assert tuplets[0].lilypond_format == "{\n\tc'8.\n}"

    tuplets =selection.to_tuplets_with_ratio(2 * [1], is_diminution=True)
    assert tuplets[0].lilypond_format == "{\n\tc'16.\n\tc'16.\n}"

    tuplets =selection.to_tuplets_with_ratio(3 * [1], is_diminution=True)
    assert tuplets[0].lilypond_format == "{\n\tc'16\n\tc'16\n\tc'16\n}"

    tuplets =selection.to_tuplets_with_ratio(4 * [1], is_diminution=True)
    assert tuplets[0].lilypond_format == "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"
