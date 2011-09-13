from abjad import *


def test_measuretools_fill_measures_in_expr_with_full_measure_spacer_skips_01():
    '''Populate nonbinary measure with time-scaled skip.'''

    t = Measure((5, 18), [])
    measuretools.fill_measures_in_expr_with_full_measure_spacer_skips(t)

    r'''
    {
        \time 5/18
        \scaleDurations #'(8 . 9) {
            s1 * 5/16
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\ts1 * 5/16\n\t}\n}"


def test_measuretools_fill_measures_in_expr_with_full_measure_spacer_skips_02():
    '''Populate measures conditionally.
        Iteration control tests index of iteration.'''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

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
        {
            \time 2/8
            b'8
            c''8
        }
    }
    '''

    def iterctrl(measure, i):
        return i % 2 == 1

    measuretools.fill_measures_in_expr_with_full_measure_spacer_skips(t, iterctrl)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            s1 * 1/4
        }
        {
            \time 2/8
            g'8
            a'8
        }
        {
            \time 2/8
            s1 * 1/4
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\ts1 * 1/4\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\ts1 * 1/4\n\t}\n}"


def test_measuretools_fill_measures_in_expr_with_full_measure_spacer_skips_03():
    '''Populate measures conditionally.
        Iteration control tests measure length.'''

    t = Staff([
        Measure((2, 8), "c'8 d'8"),
        Measure((3, 8), "c'8 d'8 e'8"),
        Measure((4, 8), "c'8 d'8 e'8 f'8"),
        ])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 3/8
            c'8
            d'8
            e'8
        }
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }
    }
    '''

    measuretools.fill_measures_in_expr_with_full_measure_spacer_skips(t, lambda m, i: 2 < len(m))

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 3/8
            s1 * 3/8
        }
        {
            \time 4/8
            s1 * 1/2
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 3/8\n\t\ts1 * 3/8\n\t}\n\t{\n\t\t\\time 4/8\n\t\ts1 * 1/2\n\t}\n}"
