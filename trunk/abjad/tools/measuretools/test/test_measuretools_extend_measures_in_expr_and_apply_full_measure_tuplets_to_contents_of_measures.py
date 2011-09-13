from abjad import *


def test_measuretools_extend_measures_in_expr_and_apply_full_measure_tuplets_to_contents_of_measures_01():
    '''Tupletize one measure, supplement one note.'''

    t = Measure((4, 8), notetools.make_repeated_notes(4))
    measuretools.extend_measures_in_expr_and_apply_full_measure_tuplets_to_measure_contents(
        t, notetools.make_repeated_notes(1))

    r'''
    {
        \time 4/8
        \times 4/5 {
            c'8
            c'8
            c'8
            c'8
            c'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 4/8\n\t\\times 4/5 {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n}"


def test_measuretools_extend_measures_in_expr_and_apply_full_measure_tuplets_to_contents_of_measures_02():
    '''Tupletize one measure, supplement one rest.'''

    t = Measure((4, 8), notetools.make_repeated_notes(4))
    measuretools.extend_measures_in_expr_and_apply_full_measure_tuplets_to_measure_contents(
        t, [Rest((1, 4))])

    r'''
    {
        \time 4/8
        \times 2/3 {
            c'8
            c'8
            c'8
            c'8
            r4
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 4/8\n\t\\times 2/3 {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tr4\n\t}\n}"
