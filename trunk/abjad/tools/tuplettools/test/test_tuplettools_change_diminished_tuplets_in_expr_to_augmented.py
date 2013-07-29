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
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 4/3 {
        c'16
        d'16
        e'16
    }
    '''

    assert inspect(tuplet).is_well_formed()
    assert tuplet.lilypond_format == "\\tweak #'text #tuplet-number::calc-fraction-text\n\\times 4/3 {\n\tc'16\n\td'16\n\te'16\n}"
