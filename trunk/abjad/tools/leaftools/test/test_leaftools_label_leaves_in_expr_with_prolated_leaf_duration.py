from abjad import *


def test_leaftools_label_leaves_in_expr_with_prolated_leaf_duration_01():

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    leaftools.label_leaves_in_expr_with_prolated_leaf_duration(t)

    r'''
    \times 2/3 {
        c'8
            _ \markup {
                \small
                    1/12
                }
        d'8
            _ \markup {
                \small
                    1/12
                }
        e'8
            _ \markup {
                \small
                    1/12
                }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\times 2/3 {\n\tc'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t1/12\n\t\t\t}\n\td'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t1/12\n\t\t\t}\n\te'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t1/12\n\t\t\t}\n}"
