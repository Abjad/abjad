from abjad import *


def test_containertools_remove_leafless_containers_in_expr_01():

    staff = Staff(Container(notetools.make_repeated_notes(2)) * 4)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff.leaves)
    beamtools.BeamSpanner(staff[:])
    containertools.delete_contents_of_container(staff[1])
    containertools.delete_contents_of_container(staff[-1])

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
        }
        {
            g'8
            a'8 ]
        }
        {
        }
    }
    '''

    containertools.remove_leafless_containers_in_expr(staff)

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
