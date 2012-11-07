from abjad import *


def test_tuplettools_fix_contents_of_tuplets_in_expr_01():
    '''Halve note durations.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'4 d'4 e'4")
    assert not t.multiplier.is_proper_tuplet_multiplier

    r'''
    \times 1/3 {
        c'4
        d'4
        e'4
    }
    '''

    tuplettools.fix_contents_of_tuplets_in_expr(t)

    r'''
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.multiplier.is_proper_tuplet_multiplier
    assert t.lilypond_format == "\\times 2/3 {\n\tc'8\n\td'8\n\te'8\n}"


def test_tuplettools_fix_contents_of_tuplets_in_expr_02():
    '''Double note duration.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'32 d'32 e'32")
    assert not t.multiplier.is_proper_tuplet_multiplier

    r'''
    \times 8/3 {
        c'32
        d'32
        e'32
    }
    '''

    tuplettools.fix_contents_of_tuplets_in_expr(t)

    r'''
    \fraction \times 4/3 {
        c'16
        d'16
        e'16
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.multiplier.is_proper_tuplet_multiplier
    assert t.lilypond_format == "\\fraction \\times 4/3 {\n\tc'16\n\td'16\n\te'16\n}"


def test_tuplettools_fix_contents_of_tuplets_in_expr_03():
    '''Halve note durations.'''

    t = tuplettools.FixedDurationTuplet(Duration(5, 16), "c'4 d'4 e'4")
    assert not t.multiplier.is_proper_tuplet_multiplier

    r'''
    \fraction \times 5/12 {
        c'4
        d'4
        e'4
    }
    '''

    tuplettools.fix_contents_of_tuplets_in_expr(t)

    r'''
    \fraction \times 5/6 {
        c'8
        d'8
        e'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.multiplier.is_proper_tuplet_multiplier
    assert t.lilypond_format == "\\fraction \\times 5/6 {\n\tc'8\n\td'8\n\te'8\n}"
