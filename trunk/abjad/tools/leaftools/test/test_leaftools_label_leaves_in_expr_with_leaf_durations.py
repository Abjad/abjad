from abjad import *


def test_leaftools_label_leaves_in_expr_with_leaf_durations_01( ):

   t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
   leaftools.label_leaves_in_expr_with_leaf_durations(t)

   r'''
   \times 2/3 {
      c'8 _ \markup { \column { \small 1/8 \small 1/12 } }
      d'8 _ \markup { \column { \small 1/8 \small 1/12 } }
      e'8 _ \markup { \column { \small 1/8 \small 1/12 } }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\times 2/3 {\n\tc'8 _ \\markup { \\column { \\small 1/8 \\small 1/12 } }\n\td'8 _ \\markup { \\column { \\small 1/8 \\small 1/12 } }\n\te'8 _ \\markup { \\column { \\small 1/8 \\small 1/12 } }\n}"
