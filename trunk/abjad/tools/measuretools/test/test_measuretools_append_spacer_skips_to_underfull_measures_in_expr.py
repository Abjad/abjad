from abjad import *


def test_measuretools_append_spacer_skips_to_underfull_measures_in_expr_01():

    t = Staff(Measure((3, 8), "c'8 d'8 e'8") * 3)
    contexttools.detach_time_signature_marks_attached_to_component(t[1])
    contexttools.TimeSignatureMark((4, 8))(t[1])
    contexttools.detach_time_signature_marks_attached_to_component(t[2])
    contexttools.TimeSignatureMark((5, 8))(t[2])

    assert not t[0].is_underfull
    assert t[1].is_underfull
    assert t[2].is_underfull

    measuretools.append_spacer_skips_to_underfull_measures_in_expr(t)

    r'''
    \new Staff {
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
            s1 * 1/8
        }
        {
            \time 5/8
            c'8
            d'8
            e'8
            s1 * 1/4
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/8\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n\t{\n\t\t\\time 4/8\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\ts1 * 1/8\n\t}\n\t{\n\t\t\\time 5/8\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\ts1 * 1/4\n\t}\n}"
