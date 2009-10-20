from abjad import *


def test_label_leaf_numbers_01( ):
   '''Leaf numbers start at 1.'''

   t = Staff(construct.scale(4))
   label.leaf_numbers(t)

   r'''
   \new Staff {
           c'8 _ \markup { \small 1 }
           d'8 _ \markup { \small 2 }
           e'8 _ \markup { \small 3 }
           f'8 _ \markup { \small 4 }
   } 
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 _ \\markup { \\small 1 }\n\td'8 _ \\markup { \\small 2 }\n\te'8 _ \\markup { \\small 3 }\n\tf'8 _ \\markup { \\small 4 }\n}"
