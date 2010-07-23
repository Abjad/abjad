from abjad import *


def test_leaftools_label_leaves_in_expr_with_leaf_duration_01( ):
   '''Label written duration of every leaf.'''

   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   leaftools.label_leaves_in_expr_with_leaf_duration(t, ['written'])

   r'''
   \times 2/3 {
      c'8 _ \markup { \small 1/8 }
      d'8 _ \markup { \small 1/8 }
      e'8 _ \markup { \small 1/8 }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\times 2/3 {\n\tc'8 _ \\markup { \\small 1/8 }\n\td'8 _ \\markup { \\small 1/8 }\n\te'8 _ \\markup { \\small 1/8 }\n}"


def test_leaftools_label_leaves_in_expr_with_leaf_duration_02( ):
   '''Label prolated duration of every leaf.'''

   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   leaftools.label_leaves_in_expr_with_leaf_duration(t, ['prolated'])

   r'''
   \times 2/3 {
      c'8 _ \markup { \small 1/12 }
      d'8 _ \markup { \small 1/12 }
      e'8 _ \markup { \small 1/12 }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\times 2/3 {\n\tc'8 _ \\markup { \\small 1/12 }\n\td'8 _ \\markup { \\small 1/12 }\n\te'8 _ \\markup { \\small 1/12 }\n}"


def test_leaftools_label_leaves_in_expr_with_leaf_duration_03( ):
   ''''Label written and prolated duration of every leaf.'''

   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   leaftools.label_leaves_in_expr_with_leaf_duration(t, ['written', 'prolated'])

   r'''
   \times 2/3 {
      c'8 _ \markup { \column { \small 1/8 \small 1/12 } }
      d'8 _ \markup { \column { \small 1/8 \small 1/12 } }
      e'8 _ \markup { \column { \small 1/8 \small 1/12 } }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\times 2/3 {\n\tc'8 _ \\markup { \\column { \\small 1/8 \\small 1/12 } }\n\td'8 _ \\markup { \\column { \\small 1/8 \\small 1/12 } }\n\te'8 _ \\markup { \\column { \\small 1/8 \\small 1/12 } }\n}"
