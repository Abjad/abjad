from abjad import *


def test_labeltools_label_leaves_in_expr_with_leaf_indices_01():
    '''Leaf indices start at 0.'''

    t = Staff("c'8 d'8 e'8 f'8")
    labeltools.label_leaves_in_expr_with_leaf_indices(t)

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

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\tc'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t0\n\t\t\t}\n\td'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t1\n\t\t\t}\n\te'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t2\n\t\t\t}\n\tf'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t3\n\t\t\t}\n}"
