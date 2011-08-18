from abjad import *


def test_containertools_color_contents_of_container_01():

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
    containertools.color_contents_of_container(staff[1], 'blue')

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \override Accidental #'color = #blue
            \override Beam #'color = #blue
            \override Dots #'color = #blue
            \override NoteHead #'color = #blue
            \override Rest #'color = #blue
            \override Stem #'color = #blue
            \override TupletBracket #'color = #blue
            \override TupletNumber #'color = #blue
            \time 2/8
            e'8
            f'8
            \revert Accidental #'color
            \revert Beam #'color
            \revert Dots #'color
            \revert NoteHead #'color
            \revert Rest #'color
            \revert Stem #'color
            \revert TupletBracket #'color
            \revert TupletNumber #'color
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\override Accidental #'color = #blue\n\t\t\\override Beam #'color = #blue\n\t\t\\override Dots #'color = #blue\n\t\t\\override NoteHead #'color = #blue\n\t\t\\override Rest #'color = #blue\n\t\t\\override Stem #'color = #blue\n\t\t\\override TupletBracket #'color = #blue\n\t\t\\override TupletNumber #'color = #blue\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\revert Accidental #'color\n\t\t\\revert Beam #'color\n\t\t\\revert Dots #'color\n\t\t\\revert NoteHead #'color\n\t\t\\revert Rest #'color\n\t\t\\revert Stem #'color\n\t\t\\revert TupletBracket #'color\n\t\t\\revert TupletNumber #'color\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n}"
