from abjad import *


def test_labeltools_remove_markup_from_leaves_in_expr_01():
    '''Clear multiple pieces of down-markup.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    labeltools.label_leaves_in_expr_with_leaf_durations(t)

    r'''
    \times 2/3 {
        c'8 _ \markup { \column { \small 1/8 \small 1/12 } }
        d'8 _ \markup { \column { \small 1/8 \small 1/12 } }
        e'8 _ \markup { \column { \small 1/8 \small 1/12 } }
    }
    '''

    labeltools.remove_markup_from_leaves_in_expr(t)

    r'''
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\times 2/3 {\n\tc'8\n\td'8\n\te'8\n}"
