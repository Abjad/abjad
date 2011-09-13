from abjad import *


def test_leaftools_label_leaves_in_expr_with_leaf_indices_01():
    '''Leaf indices start at 0.'''

    t = Staff("c'8 d'8 e'8 f'8")
    leaftools.label_leaves_in_expr_with_leaf_indices(t)

    r'''
    \new Staff {
      c'8 _ \markup { \small 0 }
      d'8 _ \markup { \small 1 }
      e'8 _ \markup { \small 2 }
      f'8 _ \markup { \small 3 }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 _ \\markup { \\small 0 }\n\td'8 _ \\markup { \\small 1 }\n\te'8 _ \\markup { \\small 2 }\n\tf'8 _ \\markup { \\small 3 }\n}"
