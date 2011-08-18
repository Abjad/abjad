from abjad import *


def test_containertools_replace_contents_of_target_container_with_contents_of_source_container_01():

    staff = Staff(Tuplet(Fraction(2, 3), "c'8 d'8 e'8") * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
    spannertools.BeamSpanner(staff.leaves)

    r'''
    \new Staff {
        \times 2/3 {
            c'8 [
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
        \times 2/3 {
            b'8
            c''8
            d''8 ]
        }
    }
    '''

    container = Container("c'8 d'8 e'8")
    spannertools.SlurSpanner(container.leaves)

    r'''
    {
        c'8 (
        d'8
        e'8 )
    }
    '''

    containertools.replace_contents_of_target_container_with_contents_of_source_container(
        staff[1], container)

    r'''
    \new Staff {
        \times 2/3 {
            c'8 [
            d'8
            e'8
        }
        \times 2/3 {
            c'8 (
            d'8
            e'8 )
        }
        \times 2/3 {
            b'8
            c''8
            d''8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tc'8 (\n\t\td'8\n\t\te'8 )\n\t}\n\t\\times 2/3 {\n\t\tb'8\n\t\tc''8\n\t\td''8 ]\n\t}\n}"
