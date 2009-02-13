from abjad import *


def test_label_leaf_durations_01( ):
   '''Label written duration of every leaf.'''

   t = FixedDurationTuplet((2, 8), scale(3))
   label_leaf_durations(t, ['written'])

   r'''
   \times 2/3 {
      c'8 _ \markup { \small 1/8 }
      d'8 _ \markup { \small 1/8 }
      e'8 _ \markup { \small 1/8 }
   }
   '''

   assert check(t)
   assert t.format == "\\times 2/3 {\n\tc'8 _ \\markup { \\small 1/8 }\n\td'8 _ \\markup { \\small 1/8 }\n\te'8 _ \\markup { \\small 1/8 }\n}"


def test_label_leaf_durations_02( ):
   '''Label prolated duration of every leaf.'''

   t = FixedDurationTuplet((2, 8), scale(3))
   label_leaf_durations(t, ['prolated'])

   r'''
   \times 2/3 {
      c'8 _ \markup { \small 1/12 }
      d'8 _ \markup { \small 1/12 }
      e'8 _ \markup { \small 1/12 }
   }
   '''

   assert check(t)
   assert t.format == "\\times 2/3 {\n\tc'8 _ \\markup { \\small 1/12 }\n\td'8 _ \\markup { \\small 1/12 }\n\te'8 _ \\markup { \\small 1/12 }\n}"


def test_label_leaf_durations_03( ):
   ''''Label written and prolated duration of every leaf.'''

   t = FixedDurationTuplet((2, 8), scale(3))
   label_leaf_durations(t, ['written', 'prolated'])

   r'''
   \times 2/3 {
      c'8 _ \markup { \column { \small 1/8 \small 1/12 } }
      d'8 _ \markup { \column { \small 1/8 \small 1/12 } }
      e'8 _ \markup { \column { \small 1/8 \small 1/12 } }
   }
   '''

   assert check(t)
   assert t.format == "\\times 2/3 {\n\tc'8 _ \\markup { \\column { \\small 1/8 \\small 1/12 } }\n\td'8 _ \\markup { \\column { \\small 1/8 \\small 1/12 } }\n\te'8 _ \\markup { \\column { \\small 1/8 \\small 1/12 } }\n}"
