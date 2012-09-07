from abjad import *


def test_labeltools_label_leaves_in_expr_with_leaf_durations_01():

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    labeltools.label_leaves_in_expr_with_leaf_durations(t)

    r'''
    \new Staff {
        c'8
            _ \markup {
                \small
                    0
                }
        d'8
            _ \markup {
                \small
                    1
                }
        e'8
            _ \markup {
                \small
                    2
                }
        f'8
            _ \markup {
                \small
                    3
                }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\times 2/3 {\n\tc'8\n\t\t_ \\markup {\n\t\t\t\\column\n\t\t\t\t{\n\t\t\t\t\t\\small\n\t\t\t\t\t\t1/8\n\t\t\t\t\t\\small\n\t\t\t\t\t\t1/12\n\t\t\t\t}\n\t\t\t}\n\td'8\n\t\t_ \\markup {\n\t\t\t\\column\n\t\t\t\t{\n\t\t\t\t\t\\small\n\t\t\t\t\t\t1/8\n\t\t\t\t\t\\small\n\t\t\t\t\t\t1/12\n\t\t\t\t}\n\t\t\t}\n\te'8\n\t\t_ \\markup {\n\t\t\t\\column\n\t\t\t\t{\n\t\t\t\t\t\\small\n\t\t\t\t\t\t1/8\n\t\t\t\t\t\\small\n\t\t\t\t\t\t1/12\n\t\t\t\t}\n\t\t\t}\n}"
