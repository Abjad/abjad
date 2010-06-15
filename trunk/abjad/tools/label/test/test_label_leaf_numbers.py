from abjad import *


def test_label_leaf_numbers_01( ):
   '''Leaf numbers start at 1.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   label.leaf_numbers(t)

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


def test_label_leaf_numbers_02( ):
   '''Optional direction keyword.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   label.leaf_numbers(t, direction = 'above')

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
