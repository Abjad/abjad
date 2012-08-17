from abjad import *


def test_measuretools_multiply_contents_of_measures_in_expr_01():
    '''Multiply contents of measure 3 times.
    '''

    t = Measure((3, 8), "c'8 d'8 e'8")
    measuretools.multiply_contents_of_measures_in_expr(t, 3)

    r'''
    {
        \time 9/8
        c'8
        d'8
        e'8
        c'8
        d'8
        e'8
        c'8
        d'8
        e'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 9/8\n\tc'8\n\td'8\n\te'8\n\tc'8\n\td'8\n\te'8\n\tc'8\n\td'8\n\te'8\n}"


def test_measuretools_multiply_contents_of_measures_in_expr_02():
    '''Multiply contents of each measure 3 times.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            e'8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    measuretools.multiply_contents_of_measures_in_expr(t, 2)

    r'''
    \new Staff {
        {
            \time 4/8
            c'8
            d'8
            c'8
            d'8
        }
        {
            \time 4/8
            e'8
            f'8
            e'8
            f'8
        }
        {
            \time 4/8
            g'8
            a'8
            g'8
            a'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 4/8\n\t\tc'8\n\t\td'8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 4/8\n\t\te'8\n\t\tf'8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\t\\time 4/8\n\t\tg'8\n\t\ta'8\n\t\tg'8\n\t\ta'8\n\t}\n}"
