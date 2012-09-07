from abjad import *


def test_labeltools_label_leaves_in_expr_with_leaf_numbers_01():
    '''Leaf numbers start at 1.'''

    t = Staff("c'8 d'8 e'8 f'8")
    labeltools.label_leaves_in_expr_with_leaf_numbers(t)

    r'''
    \new Staff {
        c'8
            _ \markup {
                \small
                    1
                }
        d'8
            _ \markup {
                \small
                    2
                }
        e'8
            _ \markup {
                \small
                    3
                }
        f'8
            _ \markup {
                \small
                    4
                }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\tc'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t1\n\t\t\t}\n\td'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t2\n\t\t\t}\n\te'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t3\n\t\t\t}\n\tf'8\n\t\t_ \\markup {\n\t\t\t\\small\n\t\t\t\t4\n\t\t\t}\n}"


def test_labeltools_label_leaves_in_expr_with_leaf_numbers_02():
    '''Optional markup direction keyword.'''

    t = Staff("c'8 d'8 e'8 f'8")
    labeltools.label_leaves_in_expr_with_leaf_numbers(t, markup_direction=Up)

    r'''
    \new Staff {
        c'8
            ^ \markup {
                \small
                    1
                }
        d'8
            ^ \markup {
                \small
                    2
                }
        e'8
            ^ \markup {
                \small
                    3
                }
        f'8
            ^ \markup {
                \small
                    4
                }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\tc'8\n\t\t^ \\markup {\n\t\t\t\\small\n\t\t\t\t1\n\t\t\t}\n\td'8\n\t\t^ \\markup {\n\t\t\t\\small\n\t\t\t\t2\n\t\t\t}\n\te'8\n\t\t^ \\markup {\n\t\t\t\\small\n\t\t\t\t3\n\t\t\t}\n\tf'8\n\t\t^ \\markup {\n\t\t\t\\small\n\t\t\t\t4\n\t\t\t}\n}"
