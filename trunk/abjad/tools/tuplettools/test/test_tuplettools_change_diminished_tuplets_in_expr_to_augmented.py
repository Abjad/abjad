from abjad import *


def test_tuplettools_change_diminished_tuplets_in_expr_to_augmented_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    r'''
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    tuplettools.change_diminished_tuplets_in_expr_to_augmented(tuplet)

    r'''
    \fraction \times 4/3 {
        c'16
        d'16
        e'16
    }
    '''

    assert componenttools.is_well_formed_component(tuplet)
    assert tuplet.format == "\\fraction \\times 4/3 {\n\tc'16\n\td'16\n\te'16\n}"
