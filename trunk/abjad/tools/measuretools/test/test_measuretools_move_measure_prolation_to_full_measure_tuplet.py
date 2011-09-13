from abjad import *


def test_measuretools_move_measure_prolation_to_full_measure_tuplet_01():
    '''Project 3/12 meter onto measure contents.'''

    inner = tuplettools.FixedDurationTuplet(Duration(2, 16), notetools.make_repeated_notes(3, Duration(1, 16)))
    notes = notetools.make_repeated_notes(2)
    outer = tuplettools.FixedDurationTuplet(Duration(2, 8), [inner] + notes)
    t = Measure((2, 8), [outer])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure(t)

    r'''
    {
        \time 3/12
        \scaleDurations #'(2 . 3) {
            \times 2/3 {
                c'16
                d'16
                e'16
            }
            f'8
            g'8
        }
    }
    '''

    assert t.format == "{\n\t\\time 3/12\n\t\\scaleDurations #'(2 . 3) {\n\t\t\\times 2/3 {\n\t\t\tc'16\n\t\t\td'16\n\t\t\te'16\n\t\t}\n\t\tf'8\n\t\tg'8\n\t}\n}"


    measuretools.move_measure_prolation_to_full_measure_tuplet(t)

    r'''
    {
        \time 2/8
        \times 2/3 {
            \times 2/3 {
                c'16
                d'16
                e'16
            }
            f'8
            g'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 2/8\n\t\\times 2/3 {\n\t\t\\times 2/3 {\n\t\t\tc'16\n\t\t\td'16\n\t\t\te'16\n\t\t}\n\t\tf'8\n\t\tg'8\n\t}\n}"


def test_measuretools_move_measure_prolation_to_full_measure_tuplet_02():
    '''Project nonbinary meter onto measure with tied note values.'''

    t = Measure((5, 8), [tuplettools.FixedDurationTuplet(Duration(5, 8), "c'8 d'8 e'8 f'8 g'8 a'8")])
    measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure(t)

    r'''
    {
        \time 15/24
        \scaleDurations #'(2 . 3) {
            c'8 ~
            c'32
            d'8 ~
            d'32
            e'8 ~
            e'32
            f'8 ~
            f'32
            g'8 ~
            g'32
            a'8 ~
            a'32
        }
    }
    '''

    assert t.format == "{\n\t\\time 15/24\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8 ~\n\t\tc'32\n\t\td'8 ~\n\t\td'32\n\t\te'8 ~\n\t\te'32\n\t\tf'8 ~\n\t\tf'32\n\t\tg'8 ~\n\t\tg'32\n\t\ta'8 ~\n\t\ta'32\n\t}\n}"

    measuretools.move_measure_prolation_to_full_measure_tuplet(t)

    r'''
    {
        \time 5/8
        \fraction \times 5/6 {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 5/8\n\t\\fraction \\times 5/6 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t}\n}"
