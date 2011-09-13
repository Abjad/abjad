from abjad import *


def test_measuretools_comment_measures_in_container_with_measure_numbers_01():
    '''Label measure numbers with comments before and after each measure.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
    measuretools.comment_measures_in_container_with_measure_numbers(staff)

    r'''
    \new Staff {
        % start measure 1
        {
            \time 2/8
            c'8
            d'8
        }
        % stop measure 1
        % start measure 2
        {
            \time 2/8
            e'8
            f'8
        }
        % stop measure 2
        % start measure 3
        {
            \time 2/8
            g'8
            a'8
        }
        % stop measure 3
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\t% start measure 1\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t% stop measure 1\n\t% start measure 2\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t}\n\t% stop measure 2\n\t% start measure 3\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t% stop measure 3\n}"


def test_measuretools_comment_measures_in_container_with_measure_numbers_02():
    '''Works on measures, too, in addition to contexts.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
    measuretools.comment_measures_in_container_with_measure_numbers(staff[1])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        % start measure 2
        {
            \time 2/8
            e'8
            f'8
        }
        % stop measure 2
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t% start measure 2\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t}\n\t% stop measure 2\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n}"
