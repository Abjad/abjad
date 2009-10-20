from abjad import *


def test_label_leaf_pitch_numbers_01( ):
   '''Works on notes, rests and chords.'''

   leaves = construct.leaves([None, 12, (13, 14, 15), None], [(1, 4)])
   t = Staff(leaves)
   label.leaf_pitch_numbers(t)

   r'''
   \new Staff {
           r4
           c''4 _ \markup { \small 12 }
           <cs'' d'' ef''>4 _ \markup { \column { \small 15 \small 14 \small 13 } }
           r4
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tr4\n\tc''4 _ \\markup { \\small 12 }\n\t<cs'' d'' ef''>4 _ \\markup { \\column { \\small 15 \\small 14 \\small 13 } }\n\tr4\n}"
