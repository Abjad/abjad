# -*- encoding: utf-8 -*-
from abjad import *


def test_TupletSelection_scale_contents_01():
    r'''Double tuplet.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    selection = selectiontools.select_tuplets(t)
    selection.scale_contents(Multiplier(2))

    r'''
    \times 2/3 {
        c'4
        d'4
        e'4
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\times 2/3 {\n\tc'4\n\td'4\n\te'4\n}"


def test_TupletSelection_scale_contents_02():
    r'''Halve tuplet.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    selection = selectiontools.select_tuplets(t)
    selection.scale_contents(Multiplier(1, 2))

    r'''
    \times 2/3 {
        c'16
        d'16
        e'16
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\times 2/3 {\n\tc'16\n\td'16\n\te'16\n}"


def test_TupletSelection_scale_contents_03():
    r'''Quadruple tuplet.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    selection = selectiontools.select_tuplets(t)
    selection.scale_contents(Multiplier(4))

    r'''
    \times 2/3 {
        c'2
        d'2
        e'2
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\times 2/3 {\n\tc'2\n\td'2\n\te'2\n}"


def test_TupletSelection_scale_contents_04():
    r'''Quarter tuplet.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    selection = selectiontools.select_tuplets(t)
    selection.scale_contents(Multiplier(1, 4))

    r'''
    \times 2/3 {
        c'32
        d'32
        e'32
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\times 2/3 {\n\tc'32\n\td'32\n\te'32\n}"


def test_TupletSelection_scale_contents_05():
    r'''Multiply tuplet by 3/2.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    selection = selectiontools.select_tuplets(t)
    selection.scale_contents(Multiplier(3, 2))

    r'''
    \times 2/3 {
        c'8.
        d'8.
        e'8.
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\times 2/3 {\n\tc'8.\n\td'8.\n\te'8.\n}"


def test_TupletSelection_scale_contents_06():
    r'''Multiply tuplet by 2/3.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    selection = selectiontools.select_tuplets(t)
    selection.scale_contents(Multiplier(2, 3))

    r'''
    \times 8/9 {
        c'16
        d'16
        e'16
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\times 8/9 {\n\tc'16\n\td'16\n\te'16\n}"


def test_TupletSelection_scale_contents_07():
    r'''Multiply tuplet by 3/5.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    selection = selectiontools.select_tuplets(t)
    selection.scale_contents(Multiplier(3, 5))

    r'''
    \times 4/5 {
        c'16
        d'16
        e'16
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\times 4/5 {\n\tc'16\n\td'16\n\te'16\n}"


def test_TupletSelection_scale_contents_08():
    r'''Multiply undotted, unbracketted notes by 3/2; ie, add a single dot.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(3, 8), "c'8 d'8 e'8")
    selection = selectiontools.select_tuplets(t)
    selection.scale_contents(Multiplier(3, 2))

    r'''
    {
        c'8.
        d'8.
        e'8.
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "{\n\tc'8.\n\td'8.\n\te'8.\n}"


def test_TupletSelection_scale_contents_09():
    r'''Binary target duration.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(3, 8), [Note(0, (2, 8)), Note(0, (3, 8))])

    r'''
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 3/5 {
        c'4
        c'4.
    }
    '''

    selection = selectiontools.select_tuplets(t)
    selection.scale_contents(Multiplier(2, 3))

    r'''
    \times 4/5 {
        c'8
        c'8.
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\times 4/5 {\n\tc'8\n\tc'8.\n}"


def test_TupletSelection_scale_contents_10():
    r'''Target duration without power-of-two denominator.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(4, 8), [Note(0, (2, 8)), Note(0, (3, 8))])

    r'''
    \times 4/5 {
        c'4
        c'4.
    }
    '''

    selection = selectiontools.select_tuplets(t)
    selection.scale_contents(Multiplier(2, 3))

    r'''
    \times 8/15 {
        c'4
        c'4.
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\times 8/15 {\n\tc'4\n\tc'4.\n}"
