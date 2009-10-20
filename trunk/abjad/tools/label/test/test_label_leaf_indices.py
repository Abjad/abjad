from abjad import *


def test_label_leaf_indices_01( ):
   '''Leaf indices start at 0.'''

   t = Staff(construct.scale(4))
   label.leaf_indices(t)

   r'''
   \new Staff {
           c'8 _ \markup { \small 0 }
           d'8 _ \markup { \small 1 }
           e'8 _ \markup { \small 2 }
           f'8 _ \markup { \small 3 }
   } 
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 _ \\markup { \\small 0 }\n\td'8 _ \\markup { \\small 1 }\n\te'8 _ \\markup { \\small 2 }\n\tf'8 _ \\markup { \\small 3 }\n}"
