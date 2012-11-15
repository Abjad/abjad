from abjad import *


def test_TaleaRhythmMaker_tie_split_notes_01():

    maker = rhythmmakertools.TaleaRhythmMaker([5], 16, tie_split_notes=True)
    divisions = [(2, 8), (2, 8), (2, 8), (2, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
    staff = Staff(measures)
    measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 2/8
            c'4 ~
        }
        {
            c'16
            c'8. ~
        }
        {
            c'8
            c'8 ~
        }
        {
            c'8.
            c'16
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'4 ~\n\t}\n\t{\n\t\tc'16\n\t\tc'8. ~\n\t}\n\t{\n\t\tc'8\n\t\tc'8 ~\n\t}\n\t{\n\t\tc'8.\n\t\tc'16\n\t}\n}"


def test_TaleaRhythmMaker_tie_split_notes_02():

    maker = rhythmmakertools.TaleaRhythmMaker([5], 16, tie_split_notes=True)
    divisions = [(3, 16), (5, 8), (4, 8), (7, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
    staff = Staff(measures)
    measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    r'''
    \new Staff {
        {
            \time 3/16
            c'8. ~
        }
        {
            \time 5/8
            c'8
            c'4 ~
            c'16
            c'8. ~
        }
        {
            \time 4/8
            c'8
            c'4 ~
            c'16
            c'16 ~
        }
        {
            \time 7/16
            c'4
            c'8.
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\tc'8. ~\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'8\n\t\tc'4 ~\n\t\tc'16\n\t\tc'8. ~\n\t}\n\t{\n\t\t\\time 4/8\n\t\tc'8\n\t\tc'4 ~\n\t\tc'16\n\t\tc'16 ~\n\t}\n\t{\n\t\t\\time 7/16\n\t\tc'4\n\t\tc'8.\n\t}\n}"
