from abjad import *


def test_leaftools_label_leaves_in_expr_with_leaf_numbers_01():
    '''Leaf numbers start at 1.'''

    t = Staff("c'8 d'8 e'8 f'8")
    leaftools.label_leaves_in_expr_with_leaf_numbers(t)

    r'''
    \new Staff {
      c'8 _ \markup { \small 1 }
      d'8 _ \markup { \small 2 }
      e'8 _ \markup { \small 3 }
      f'8 _ \markup { \small 4 }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 _ \\markup { \\small 1 }\n\td'8 _ \\markup { \\small 2 }\n\te'8 _ \\markup { \\small 3 }\n\tf'8 _ \\markup { \\small 4 }\n}"


def test_leaftools_label_leaves_in_expr_with_leaf_numbers_02():
    '''Optional markup direction keyword.'''

    t = Staff("c'8 d'8 e'8 f'8")
    leaftools.label_leaves_in_expr_with_leaf_numbers(t, markup_direction = 'up')

    r'''
    \new Staff {
      c'8 ^ \markup { \small 1 }
      d'8 ^ \markup { \small 2 }
      e'8 ^ \markup { \small 3 }
      f'8 ^ \markup { \small 4 }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 ^ \\markup { \\small 1 }\n\td'8 ^ \\markup { \\small 2 }\n\te'8 ^ \\markup { \\small 3 }\n\tf'8 ^ \\markup { \\small 4 }\n}"
