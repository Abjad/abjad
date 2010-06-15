from abjad import *


def test_label_clear_leaves_01( ):
   '''Clear multiple pieces of down-markup.'''

   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   label.leaf_durations(t)

   r'''
   \times 2/3 {
      c'8 _ \markup { \column { \small 1/8 \small 1/12 } }
      d'8 _ \markup { \column { \small 1/8 \small 1/12 } }
      e'8 _ \markup { \column { \small 1/8 \small 1/12 } }
   }
   '''

   label.clear_leaves(t)
   
   r'''
   \times 2/3 {
      c'8
      d'8
      e'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\times 2/3 {\n\tc'8\n\td'8\n\te'8\n}"
