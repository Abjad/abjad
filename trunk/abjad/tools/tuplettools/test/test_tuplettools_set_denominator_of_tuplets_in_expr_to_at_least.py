from abjad import *


def test_tuplettools_set_denominator_of_tuplets_in_expr_to_at_least_01():

    tuplet = Tuplet(Fraction(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplettools.set_denominator_of_tuplets_in_expr_to_at_least(tuplet, 8)

    r'''
    \fraction \times 6/10 {
        c'4
        d'8
        e'8
        f'4
        g'2
    }
    '''

    assert tuplet.format == "\\fraction \\times 6/10 {\n\tc'4\n\td'8\n\te'8\n\tf'4\n\tg'2\n}"


def test_tuplettools_set_denominator_of_tuplets_in_expr_to_at_least_02():

    tuplet = Tuplet(Fraction(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplettools.set_denominator_of_tuplets_in_expr_to_at_least(tuplet, 16)

    r'''
    \fraction \times 12/20 {
        c'4
        d'8
        e'8
        f'4
        g'2
    }
    '''

    assert tuplet.format == "\\fraction \\times 12/20 {\n\tc'4\n\td'8\n\te'8\n\tf'4\n\tg'2\n}"


def test_tuplettools_set_denominator_of_tuplets_in_expr_to_at_least_03():

    tuplet = Tuplet(Fraction(3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplettools.set_denominator_of_tuplets_in_expr_to_at_least(tuplet, 2)

    r'''
    \fraction \times 3/5 {
        c'4
        d'8
        e'8
        f'4
        g'2
    }
    '''

    assert tuplet.format == "\\fraction \\times 3/5 {\n\tc'4\n\td'8\n\te'8\n\tf'4\n\tg'2\n}"
