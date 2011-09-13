from abjad import *


def test_tuplettools_change_augmented_tuplets_in_expr_to_diminished_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'8 d'8 e'8")

    r'''
    \times 4/3 {
        c'8
        d'8
        e'8
    }
    '''

    tuplettools.change_augmented_tuplets_in_expr_to_diminished(tuplet)

    r'''
    \times 2/3 {
        c'4
        d'4
        e'4
    }
    '''

    assert componenttools.is_well_formed_component(tuplet)
    assert tuplet.format == "\\times 2/3 {\n\tc'4\n\td'4\n\te'4\n}"
